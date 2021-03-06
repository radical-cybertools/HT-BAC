import os
import sys
import datetime
import radical.pilot

def chop_microseconds(delta):
    return delta - datetime.timedelta(microseconds=delta.microseconds)

DBURL = os.getenv("RADICAL_PILOT_DBURL")
if DBURL is None:
    print "ERROR: radical.pilot_DBURL (MongoDB server URL) is not defined."
    sys.exit(1)
    
DBNAME = 'radical-ensemblemd-htbac-fecalc-benchmark'

SESSION_IDS = {
               "16": [
                    # TLP: 16
                    "53aabce10941dee864207d65",
                    "53aabd610941dee864207d6a",
                    "53aabe0e0941dee864207d70",
                    "53aabe970941dee864207d78",
                    "53aabfdd0941dee864207d84",
                    "53aac09e0941dee864207d98",
                    "53aac1cf0941dee864207dbc",
                     ],

               "8" : [
                    # TLP: 8
                    "53aa77f40941deb22e580484",
                    "53aa788b0941deb22e58048a",
                    "53aa79290941deb22e580492",
                    "53aa79cf0941deb22e58049e",
                    "53aa7a7f0941deb22e5804b2",
                    "53aa7b3c0941deb22e5804d6",
                    "53aa7c220941deb22e58051a"],


                "4" : [
                    # TLP: 4
                    "53aa842b0941deb3eef861df",
                    "53aa84fb0941deb3eef861e7",
                    "53aa85f60941deb3eef861f3",
                    "53aa86f00941deb3eef86207",
                    "53aa882e0941deb3eef8622b",
                    "53aa89720941deb3eef8626f",
                    "53aa8ad70941deb3eef862f3",],


                "2" : [
                    # TLP 2
                    "53aaac210941deb6c48e4735",
                    "53aaad6a0941deb6c48e4741",
                    "53aaaeb90941deb6c48e4755",
                    "53aab0210941deb6c48e4779",
                    "53aab1ae0941deb6c48e47bd",
                    "53aab7e40941deb6c48e4841",
                    "53aac3ed0941de0fd7913e9c"
                    ],


                "1" : [
                    # TLP 1
                    "53aacfe70941de414c3f9f7b",
                    "53aad24a0941de414c3f9f8f",
                    "53aad4a70941de414c3f9fb3",
                    "53aad8970941de414c3f9ff7",
                    "53aadb6e0941de414c3fa07b",
                    "53aadee20941de414c3fa17f",
                    "53aae3850941de414c3fa383"
                    ]
                }

try:

    # NOW LET'S TRY TO RECONENCT
    for tlp, session_ids in SESSION_IDS.iteritems():
        #print "TLP: %s" % tlp
        for session_id in session_ids:
            session = radical.pilot.Session(database_url=DBURL, database_name=DBNAME, session_uid=session_id)

            pm = session.get_pilot_managers()[0]
            pilot = pm.get_pilots()[0]
            pilot_cores = pilot.description['cores']

            um = session.get_unit_managers()[0]
            units = um.get_units()

            earliest_start_time = None
            latests_stop_time = None
            for unit in units:
                runtime = unit.stop_time - unit.start_time
                print "{0} {1} {2}".format(tlp, pilot_cores, runtime.seconds)
            #     if earliest_start_time is None:
            #         earliest_start_time = unit.start_time
            #     elif unit.start_time < earliest_start_time:
            #         earliest_start_time = unit.start_time

            #     if latests_stop_time is None:
            #         latests_stop_time = unit.stop_time
            #     elif unit.stop_time > latests_stop_time:
            #         latests_stop_time = unit.stop_time

            # print " * Units: %s. Exec duration %s " % (len(units), latests_stop_time - earliest_start_time)

            session.close(delete=False)

except Exception, ex:

    print "Errro {0}".format(ex)
    sys.exit(1)