import pandas as pd
import env

def get_connection(db, user=env.user, host=env.host, password=env.password):
	'''
	Open a connection to a mySQL database. The name of the database
	should be the input to this function. Make sure your database
	credentials are not included in this file.
	'''
	return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def get_zillow_prop6():
    return pd.read_sql('SELECT p6.*,\
       ac.airconditioningdesc,\
       arc.architecturalstyledesc,\
       bldg.buildingclassdesc,\
       plut.propertylandusedesc,\
       st.storydesc,\
       tct.typeconstructiondesc,\
       horst.heatingorsystemdesc\
       FROM properties_2016 AS p6\
       LEFT OUTER JOIN airconditioningtype as ac\
       ON ac.airconditioningtypeid = p6.airconditioningtypeid\
       LEFT OUTER JOIN architecturalstyletype as arc\
       ON arc.architecturalstyletypeid = p6.architecturalstyletypeid\
       LEFT OUTER JOIN buildingclasstype as bldg\
       ON bldg.buildingclasstypeid = p6.buildingclasstypeid\
       LEFT OUTER JOIN propertylandusetype as plut\
       ON plut.propertylandusetypeid = p6.propertylandusetypeid\
       LEFT OUTER JOIN storytype as st\
       ON st.storytypeid = p6.storytypeid\
       LEFT OUTER JOIN typeconstructiontype as tct\
       ON tct.typeconstructiontypeid = p6.typeconstructiontypeid\
       LEFT OUTER JOIN heatingorsystemtype as horst\
       ON horst.heatingorsystemtypeid = p6.heatingorsystemtypeid;',
       get_connection('zillow'))

def get_zillow_prop7():
    return pd.read_sql('SELECT p7.*,\
       ac.airconditioningdesc,\
       arc.architecturalstyledesc,\
       bldg.buildingclassdesc,\
       plut.propertylandusedesc,\
       st.storydesc,\
       tct.typeconstructiondesc,\
       horst.heatingorsystemdesc\
       FROM properties_2017 AS p7\
       LEFT OUTER JOIN airconditioningtype as ac\
       ON ac.airconditioningtypeid = p7.airconditioningtypeid\
       LEFT OUTER JOIN architecturalstyletype as arc\
       ON arc.architecturalstyletypeid = p7.architecturalstyletypeid\
       LEFT OUTER JOIN buildingclasstype as bldg\
       ON bldg.buildingclasstypeid = p7.buildingclasstypeid\
       LEFT OUTER JOIN propertylandusetype as plut\
       ON plut.propertylandusetypeid = p7.propertylandusetypeid\
       LEFT OUTER JOIN storytype as st\
       ON st.storytypeid = p7.storytypeid\
       LEFT OUTER JOIN typeconstructiontype as tct\
       ON tct.typeconstructiontypeid = p7.typeconstructiontypeid\
       LEFT OUTER JOIN heatingorsystemtype as horst\
       ON horst.heatingorsystemtypeid = p7.heatingorsystemtypeid;',
       get_connection('zillow'))

def get_zillow_pred6():
    return pd.read_sql('SELECT pred6.parcelid,\
		pred6.logerror,\
        pred6.transactiondate\
        FROM predictions_2016 as pred6;',
       get_connection('zillow'))

def get_zillow_pred7():
    return pd.read_sql('SELECT pred7.parcelid,\
            pred7.logerror,\
        pred7.transactiondate\
        FROM predictions_2017 as pred7;',
       get_connection('zillow'))

def save_df():
	'''
	Saves the dataframe as a csv file locally.
	'''
	get_zillow_prop6().to_csv("properties_2016.csv", index=False)
	get_zillow_prop7().to_csv("properties_2017.csv", index=False)
	get_zillow_pred6().to_csv("predictions_2016.csv", index=False)
	get_zillow_pred7().to_csv("predictions_2017.csv", index=False)


