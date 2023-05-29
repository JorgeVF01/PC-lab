import pyAgrum as gum
import numpy as np

import json

with open("request.txt","r") as file:
  request = json.load(file)

# import pyAgrum.lib.notebook as gnb

procesadores = ["AMD Ryzen 9 7950x",
                "AMD Ryzen 7 7800x3D",
                "AMD Ryzen 5 7600x",
                "Intel® Core i9",
                "Intel® Core i7",
                "Intel® Core i5"
                ]
procesadores = {v:i for i,v in enumerate(procesadores)}

placa = ["Z690",
         "H670",
         "B660",
         "X570",
         "B550",
         "A520",
         ]
placa = {v:i for i,v in enumerate(placa)}

GPU = ["RTX 4090",
      "RTX 4070",
      "RTX 3070TI",
      "RX 7900XTX",
      "RX 6800",
      "RX 6600",
       ]

GPU = {v:i for i,v in enumerate(GPU)}

refrigeracion = ["Cooler Master MasterLiquid Lite 240",
                 "NZXT Kraken 120",
                 "Mars Gaming ML360W",
                 "Cooler Master MasterLiquid ML360 Illusion",
                 "ARCTIC Liquid Freezer II 240",
                 "Corsair iCUE H150i ELITE LCD",
                 ]
refrigeracion = {v:i for i,v in enumerate(refrigeracion)}
fuentes = ["EVGA 600 GD 80 PLUS Gold",
           "Fuente NzXT C650 650 Watts 80 Plus Gold",
           "Redragon PSU007 80+ Gold 850 W",
           "RM850, 850 W, 80 Plus Gold",
           "Thermaltake Toughpower 1200W Gold",
           "Nzxt C1200 Gold 1200w",
           ]

fuentes = {v:i for i,v in enumerate(fuentes)}



def add_cpt(red,name,nickname,array):
  for i in range(6):
    red.cpt(name)[{nickname:i}] = array.T[i]

def make_inference(red,evidencia, post):
  ie=gum.LazyPropagation(red)
  ie.setEvidence(evidencia)
  ie.makeInference()
  return ie.posterior(post)





GPU_cooler = np.load("GPU_cooler.npy")
power_GPU = np.load("power_GPU.npy")
GPU_cooler = np.load("GPU_cooler.npy")
coolers_cores = np.load("coolers_cores.npy")
Gpu_cores = np.load("Gpu_cores.npy")
power_mother = np.load("power_mother.npy")
Cooler_Gpu = np.load("Cooler_Gpu.npy")
MB_cores = np.load("MB_cores.npy")
Cores_gpu = np.load("cores_gpu.npy")

mother_proba = [.3,.15,.05,.3,.15,.05]

# red uno

N = gum.BayesNet()

N = gum.BayesNet()
Coolers = N.add(gum.LabelizedVariable("C","Coolers",6))
motherboard = N.add(gum.LabelizedVariable("MB","motherboard",6))
Gpu = N.add(gum.LabelizedVariable("Gpu","Gpu",6))
power = N.add(gum.LabelizedVariable("Pw","power",6))
cores = N.add(gum.LabelizedVariable("Core","cores",6))

N.addArc(motherboard,power)
N.addArc(motherboard,cores)
N.addArc(cores,Gpu)
N.addArc(cores,Coolers)

  
N.cpt(motherboard).fillWith(mother_proba)
add_cpt(N,power,"MB",power_mother)
add_cpt(N,cores,"MB",MB_cores.T)
add_cpt(N,Coolers,"Core",coolers_cores)
add_cpt(N,Gpu,"Core",Gpu_cores)

N.cpt(cores)
N.cpt(Gpu)
N.cpt(power)
N.cpt(Coolers)
N.cpt(motherboard)




N1 = gum.BayesNet()
Coolers1 = N1.add(gum.LabelizedVariable("C","Coolers",6))
motherboard1 = N1.add(gum.LabelizedVariable("MB","motherboard",6))
Gpu1 = N1.add(gum.LabelizedVariable("Gpu","Gpu",6))
power1 = N1.add(gum.LabelizedVariable("Pw","power",6))
cores1 = N1.add(gum.LabelizedVariable("Core","cores",6))

N1.addArc(Gpu1,cores1)
N1.addArc(Gpu1,Coolers1)
N1.addArc(cores1,motherboard1)
N1.addArc(motherboard1,power1)

N1.cpt(Gpu).fillWith([.3,.15,.05,.3,.15,.05])



add_cpt(N1,cores1,"Gpu",Cores_gpu)
add_cpt(N1,Coolers1,"Gpu",Cooler_Gpu)
add_cpt(N1, motherboard1,"Core",MB_cores)
add_cpt(N1,power,"MB",power_mother)

N1.cpt(cores1)
N1.cpt(Gpu1)
N1.cpt(power1)
N1.cpt(Coolers1)
N1.cpt(motherboard1)




switches = ["sw_power","sw_gpu","sw_placa","sw_proce","sw_cooler"]
ids = ["power","gpu","placa","proce","cooler"]
networknames = ["Pw","Gpu","MB","Core","C"]
names = [fuentes,GPU,placa,procesadores,refrigeracion]
switches_ids = dict(zip(switches,ids))
ids_names = dict(zip(ids,names))
ids_networknames = dict(zip(ids,networknames))
networknames_names = dict(zip(networknames,names))

evidence = { ids_networknames[id]:ids_names[id][request[id]] for switch,id in switches_ids.items() if switch in request}
#if request["scheme"] == "Scheme_1":


missing = [ids_networknames[switches_ids[switch]] for switch in switches if switch not in request]

for i in missing:
  if request["scheme"] =="Scheme_1":
    print(json.dumps({i:dict(zip(networknames_names[i].keys(),np.around(make_inference(N,evidence,i).toarray(),4)))}))
  else:
    print(json.dumps({i:dict(zip(networknames_names[i].keys(),np.around(make_inference(N1,evidence,i).toarray(),4)))}))



