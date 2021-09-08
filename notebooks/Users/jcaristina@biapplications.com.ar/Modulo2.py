# Databricks notebook source
# MAGIC %md
# MAGIC Para ejecutar el codigo del modulo2, primero deberan instalar la ultima version de la libreria https://pypi.org/project/line-profiler/
# MAGIC 
# MAGIC Para declarar la ultima version, deberan utilizar el signo "==" para indicarle al cluster que instale la ultima version. 
# MAGIC 
# MAGIC Por ejemplo: **line-profiler==3.3.0**

# COMMAND ----------

# MAGIC %md
# MAGIC Una vez que este instalado, podemos importar las librerias que necesitamos para este modulo:

# COMMAND ----------

import inspect
from io import StringIO
from line_profiler import LineProfiler

# COMMAND ----------

# MAGIC %md
# MAGIC Este codigo no solo hace in import de la libreria que instalamos, sino tambien de otras que ya vienen preinstaladas en el Runtime de Azure Databricks.

# COMMAND ----------

def profile_function(my_func, *args, **kwargs):
  lp = LineProfiler()
  output_val = lp(my_func)(*args, **kwargs)
  mystdout = StringIO()
  lp.print_stats(stream=mystdout) #Redirect stdout so we can grab profile output
  lprof_lines = mystdout.getvalue().split('\n')
  profile_start = 1 + next(idx for idx, line in enumerate(lprof_lines) if '=====' in line)
  lprof_code_lines = lprof_lines[profile_start:-1]
  source_lines = inspect.getsource(my_func).split('\n')

  if len(source_lines) != len(lprof_code_lines):
    print("WARNING! Mismatch in source length and returned line profiler estimates")
    print('\n'.join(lprof_lines))
    print("---- Code ----")
    print(source)
  else:
    print("\n".join(lprof_lines[:profile_start]))
    print("\n".join(["{0} \t {1}".format(l, s) for l, s in zip(lprof_code_lines, source_lines)]))

  return output_val

# COMMAND ----------

# MAGIC %md
# MAGIC Declaramos dos funciones, el primero se encarga de medir y mostrar el rendimiento del codigo dentro de una funcion. El segundo es una funcion simple que utilizaremos como ejemplo para medir la velocidad.

# COMMAND ----------

def func_to_test(inner, outer):
    count = 0
    for a in range(outer):
        for b in range(inner):
            count += 1
    return count

# COMMAND ----------

profile_function(func_to_test, 3, outer=5)

# COMMAND ----------

# MAGIC %md
# MAGIC Una vez que ejecutaron el notebook, pueden desinstalar la libreria!