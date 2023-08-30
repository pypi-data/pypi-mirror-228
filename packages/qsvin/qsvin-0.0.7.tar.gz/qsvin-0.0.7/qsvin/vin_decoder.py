from .db_client import *
from .external_api import *


def insertValsToHive(data):
    vals=[]
    for k,v in data.items():
        if k in ('other','year'): continue
        vals.append(f"\'{v}\'") if v else vals.append(f"NULL")
    return vals

class VinDecoder:
    def __init__(self, connector):
        self._db_connector =  QHiveConnector("qirevin.out_db", connector)
        self._db_backup_connector = QHiveConnector("qirevin.backup_out_db", connector)
    
        self._vin_parser = VinInfo()

        self._vin_external_api=[VinNHTSA()]

    def _spark2pandas(self, df):
        return df.to_pandas() if type(df).__name__ == 'Table' else df.toPandas()
        
    def lookup_vin(self, vin, query=None, hierarchical=False):
        if all([vin,query]) or not any([vin,query]): Exception('ValueError. Use either vin or query')
        if query: return self._spark2pandas(self._db_connector.selectObj("*", query))
        if isinstance(vin, str): vin=[vin]
        result=[]
        for v in vin:
            try:
                decoded_vin = self._parse_vin(v,hierarchical)
                if decoded_vin is not None: result.append(decoded_vin)
            except Exception as e: 
                print(e)
                continue
        if len(result)==0: return None
        elif len(result)==1: return result[0]
        return pd.concat(result)

    def _parse_vin(self, v,hierarchical):
        vin_info=self._vin_parser.lookup_vin(v)
        if not vin_info: 
            print(f"Unknown {v}")
            return None
        conditions=f"vds = '{vin_info['vds']}' and wmi = '{vin_info['wmi']}' and vis = '{vin_info['vis']}'"
        if hierarchical: conditions=conditions.replace("and", "or")
        result_vin = self._spark2pandas(self._db_connector.selectObj("*", conditions)) # exact match
        if not result_vin.empty: return result_vin
        
        external_api_res = {}
        for api in self._vin_external_api:
            try: external_api_res.update(api.lookup_vin(v))
            except: continue
        insert_data={**vin_info, **external_api_res, "other": {**vin_info.get("other", {}), **external_api_res.get("other", {})}} if external_api_res else vin_info
        self._insert({k:v for k,v in insert_data.items() if v is not None}, self._db_connector)
        return self._spark2pandas(self._db_connector.selectObj("*", conditions))
    
    def export_excel(self, vin, query=None, hierarchical=False, fname="output.xlsx"):
        response = self.lookup_vin(vin=vin, query=query, hierarchical=hierarchical)
        if isinstance(response, pd.DataFrame): 
            response['date_created'] = response['date_created'].dt.tz_localize(None)
            response.to_excel(fname)
        else: Exception('ValueError. No data to write')
            
    def _create_snapshot(self, row):
        if all([row['vds'],row['wmi'],row['vis']]):
            conditions=f"vds = '{row['vds']}' and wmi = '{row['wmi']}' and vis = '{row['vis']}'"
            result_vin = self._spark2pandas(self._db_connector.selectObj("*", conditions))
            if not result_vin.empty:
                insert_data=result_vin.replace(np.nan, None).to_dict("records")[0]
                self._insert_backup({k:v for k,v in insert_data.items() if v is not None},self._db_backup_connector,"date_added_backup")
                self._db_connector.deleteObj(conditions)
        insert_data=row.to_dict()
        insert_data.pop("date_created", None)
        self._insert({k:v for k,v in insert_data.items() if v is not None}, self._db_connector)

    def _distinct(self, table, columns):
        if isinstance(columns, str): columns=[columns]
        q = f"select distinct {','.join(columns)} from {table.table}"
        return self._spark2pandas(self._db_connector.executeQuery(q)).values[:, 0]
        
    def update_db(self, data):
        if isinstance(data, str): data = pd.read_csv(data, index_col=0, low_memory=False)
        elif isinstance(data, list): data = pd.DataFrame(data)
        elif isinstance(data, dict): data = pd.DataFrame.from_dict(data)
        data.apply(lambda x: self._create_snapshot(x), axis=1)

    def _insert(self, data,table):
        data={**{k:None for k in table.columns if k != "date_created"}, **data}
        vals=','.join(insertValsToHive(data))
        q=f"""insert into table {table.table} ({','.join([x for x in data.keys() if x not in ('other', 'year', 'date_created')])},other,year,date_created) VALUES ({vals}, '{json.dumps(data.get('other', {}))}', {data.get("year", None)},current_timestamp())"""
        print(q)
        self._db_connector.executeQuery(q)

    def _insert_backup(self, data,table,date_col="date_added_backup"):
        data={**{k:None for k in table.columns if k !=date_col}, **data}
        vals=','.join(insertValsToHive(data))
        q=f"""insert into table {table.table} ({','.join([x for x in data.keys() if x not in ('other', 'year')])},other,year,{date_col}) VALUES ({vals}, '{json.dumps(data.get('other', {})) if isinstance(data.get('other', {}), dict) else data.get('other')}', {data.get("year", None)},current_timestamp())"""
        print(q)
        self._db_connector.executeQuery(q)