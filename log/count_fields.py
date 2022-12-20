import pandas as pd
import matplotlib.pyplot as plt

# field_count = input("The field name for counting:")
# field_condition = input("The field name for condition:")
# condition = input("Condition:")
# file_name = input("File name:")
field_count = "request_uri"
# field_condition = "host"
file_name = "user38610.39120bede8b01191ebcce1d729786f7d86364cd9fe7ea8320265cb4499d07d2e.csv"
# Открываем файл, читаем заголовки и находим их положения
log_table = pd.read_csv(file_name, ";")
print (log_table.info())
print((log_table[field_count].value_counts()).head(20))
((log_table[field_count].value_counts()).head(20)).plot()
plt.show()



