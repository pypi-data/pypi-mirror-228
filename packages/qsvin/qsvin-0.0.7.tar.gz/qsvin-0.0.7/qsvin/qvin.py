import logging
from .vin_decoder import *
from fuzzywuzzy import fuzz

class QVin(VinDecoder):
    _FEATURES = ['wmi','vds','vis','body_type', 'fuel_type', 'truckDB_Engine_power_bhp', 'weight']
    def __init__(self, credentials=None): 
        if credentials: 
            from .remote_client import DatabricksSQLClient
            logging.getLogger("databricks.sql").setLevel(logging.ERROR)
            connector = DatabricksSQLClient(**credentials).execute_statement
        else: 
            from pyspark.sql import SparkSession
            connector = SparkSession.builder.getOrCreate().sql
        super(QVin, self).__init__(connector)
        self._db_features = QHiveConnector("qirevin.truck_car", connector)

    def lookup_vin(self, vin, query=None, hierarchical=False, feature=False): 
        response=super().lookup_vin(vin, query=query, hierarchical=hierarchical).replace(np.nan, None)
        return self._feature_selection(self._expand_features(response)) if feature else response

    def _feature_selection(self, df):
        return df[self._FEATURES].rename(columns={"truckDB_Engine_power_bhp": "engine_power_bhp"})
    
    def get_distinct(self): return {"body_type": self._distinct(self._db_connector, 'body_type'), "fuel_type": self._distinct(self._db_connector, 'fuel_type')}
    
    def _expand_features(self, df):
        features=self._spark2pandas(self._db_features.selectObj("*"))

        def fuzzy_lookup(x, features, threshold=80):
            match_columns = {"truckDB_Model":"model", "truckDB_Serie":"serie"}
            
            def iterator(cols, x_row, f_table, fuzzy_threshold=None):
                if fuzzy_threshold is None:
                    for fcol,xcol in cols.items():
                        res = f_table[(f_table[fcol].str.lower() == str(x[xcol]).lower())]
                        if not res.empty: return res.iloc[0].squeeze()
                        else: continue
                else:
                    for idx, row in f_table.iterrows():
                        similarity_scores = [
                            fuzz.partial_ratio(str(x_row[xcol]).lower(), str(row[fcol]).lower())
                            for fcol,xcol in cols.items()
                        ]
                        if any(score >= fuzzy_threshold for score in similarity_scores):
                            return row.squeeze()
                return None
            

            condition = (features["truckDB_Make"].str.lower() == str(x['maker']).lower())
            if features[condition].empty: return pd.Series([None] * len(features.columns), index=list(features.columns))
            res=iterator(match_columns, x, features[condition])
            if res is None: res=iterator(match_columns, x, features[condition], 0.9)
            
            return res if res is not None else pd.Series([None] * len(features.columns), index=list(features.columns))

        lookup_result = df.apply(lambda x: fuzzy_lookup(x, features), axis=1)

        return pd.concat([df, lookup_result], axis=1)