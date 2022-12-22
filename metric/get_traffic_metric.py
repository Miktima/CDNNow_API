from Traffic import Traffic
import pandas as pd
import json
import matplotlib.pyplot as plt


project = input("Project ([userXXXXX]):")
objTraffic = Traffic()
result = objTraffic.get_traffic_metric(project)
result_frame = pd.read_json(json.dumps(result), "records")
plt.plot(result_frame["timestamp"], result_frame["edge_cache_status_hit_ratio"])
plt.title = "Edge cache status hit ratio"
plt.xticks(rotation='vertical')
plt.show()
input ("Another plot?")
plt.close()
plt.plot(result_frame["timestamp"], result_frame["edge_requests_count"], label="edge requests count")
plt.plot(result_frame["timestamp"], result_frame["edge_status_4xx"], label="edge status 4xx")
plt.xticks(rotation='vertical')
plt.legend()
plt.title = "Edge requests"
plt.show()
input ("Another plot?")
plt.close()
plt.plot(result_frame["timestamp"], result_frame["origin_requests_count"], label="origin requests count")
plt.plot(result_frame["timestamp"], result_frame["origin_status_4xx"], label="origin status 4xx")
plt.xticks(rotation='vertical')
plt.legend()
plt.title = "Origin requests"
plt.show()
qsave = input ("Save the data to CSV file? [Y/N]: ")
if qsave == "y":
    result_frame.to_csv("test.csv", ";")
