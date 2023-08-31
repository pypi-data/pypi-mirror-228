import numpy as np
import pandas as pd
import os, sys
import json, requests, ast
import pkg_resources
import GPUtil, platform, psutil
from datetime import datetime
from sklearn import metrics
import matplotlib.pyplot as plt
import dill
import urllib.request
from pathlib import Path
import glob, re
import shutil, yaml, random, string

try:
    import torch
except ImportError:
    pass

try:
    import keras
except ImportError:
    try:
      import tensorflow.keras as keras
    except:
      pass

try:
    import tensorflow as tf
except ImportError:
    pass
      
protocol = 'https'
IP = 'mynacode.com'


#protocol = 'http'
#IP = '127.0.0.1:8000'


username = ""
key = ""
run_id_global = ""
project_id_global = ""
run_dir_global = ""
project_dir_global = ""
prev_max = -9999999999
prev_min = 9999999999
metric_values = []
index_count = 0
model_global = None
sweep_global = False
save_best_results = False
first_sweep_run = False
dataset_dict = {}
results_dict = {}
track_config = {}
  

def login(uname, ky):
  global username
  global key
  
  print("Logging in...")
  credentials = {'username':uname, 'key':ky, 'task':'login'}
  response = requests.post(protocol+'://'+IP+'/api/python_login', data=credentials)
  
  if response.text == '1':
    username = uname
    key = ky
    print("Successfully connected to mynacode!")
  else:
    print("Credentials could not be verified.")


def metadata(run_id):

  installed_packages = pkg_resources.working_set #Save all installed packages for that project
  installed_packages_list = sorted(["%s = %s" % (i.key, i.version) for i in installed_packages])

  system_info_list = ['Codebase Python ' + platform.python_version()]
  
  system_info_list.append("    GPU    ")
  try:
      gpus = GPUtil.getGPUs()
      if len(gpus) == 0:
          system_info_list.append("No NVIDIA GPU found")
      else:
          for gpu in gpus:
            gpu_id = gpu.id
            gpu_name = gpu.name
            gpu_memory = gpu.memoryTotal
            system_info_list.append("GPU ID " + str(gpu_id))
            system_info_list.append(gpu_name)
            system_info_list.append(str(gpu_memory) + " MB")
  except:
      system_info_list.append("No NVIDIA Driver found")

  system_info_list.append("    CPU    ")
  system_info_list.append(platform.processor())
  system_info_list.append(platform.platform())
  system_info_list.append(platform.machine())
  system_info_list.append("    MEMORY    ")
  system_info_list.append("RAM " + str(round(psutil.virtual_memory().total / (1024.0 **3))) + " GB")

  data = {'run_id' : run_id, 'installed_packages': str(installed_packages_list), 'username': username, 'key': key, 'system_information': str(system_info_list)}
  
  response = requests.post(protocol+'://'+IP+'/api/add_metadata', data=data)
  
  if response.text == '0':
    print("Authentication failed")
  else:
    print("Metadata saved")


def create_project(project_name = ""):
    data = {'project_name': project_name, 'username': username, 'key': key}
    response = requests.post(protocol+'://'+IP+'/api/create_project_python', data=data)

    return response.text


def create_run(project_id = None, sweep = False, sweep_name = ""):
    if not project_id:
      print("Please provide project ID")
      return
    
    data = {'project_id': project_id, 'username': username, 'key': key, 'sweep': sweep, 'sweep_name': sweep_name}
    response = requests.post(protocol+'://'+IP+'/api/create_run_python', data=data)

    return response.text


def start(base_folder = "", project_name = ""):
  
    global project_id_global
    global project_dir_global
    global prev_max 
    global prev_min
    global metric_values
    global metric_index
    global index_count


    prev_max = -9999999999
    prev_min = 9999999999
    metric_values = []
    metric_index = 0
    index_count = 0


    if len(base_folder) == 0:
      print("Using current working directory")
      base_folder = Path.cwd().as_posix()
    elif not os.path.exists(base_folder):
      print("Using current working directory. Path not found: ", base_folder)
      base_folder = Path.cwd().as_posix()

    if not os.path.exists(base_folder+'/'+'mynacode'):
      os.mkdir(base_folder+'/mynacode')

    if len(project_name) == 0:
      project_name = 'project'

    if not os.path.exists(base_folder+'/mynacode/'+project_name):
      os.mkdir(base_folder+'/mynacode/'+project_name)
 
    project_id_global = create_project(project_name)
    project_dir_global = base_folder+'/mynacode/'+project_name      



def init(sweep = True, sweep_name = "", save_files = False):

    global run_dir_global
    global run_id_global
    global prev_max 
    global prev_min
    global metric_values
    global metric_index
    global index_count
    global first_sweep_run


    prev_max = -9999999999
    prev_min = 9999999999
    metric_values = []
    metric_index = 0
    index_count = 0

    if sweep == True:
      sweep_global = True
      first_sweep_run = True

    config_dict={}
      
    if sweep == True:
      
      if len(str(sweep_name)) > 0:
        r_id = create_run(int(project_id_global), sweep = True, sweep_name = "[S] "+sweep_name)
      else:
        r_id = create_run(int(project_id_global), sweep = True, sweep_name = "[S] Best Run")
        
      run_id_global = r_id
      run_dir_global = project_dir_global+'/Sweep_'+str(r_id)+'_'+str(datetime.now())[:10]
      os.mkdir(run_dir_global)    
    else:
      r_id = create_run(int(project_id_global))
      run_id_global = r_id
      run_dir_global = project_dir_global+'/Run_'+str(r_id)+'_'+str(datetime.now())[:10]
      os.mkdir(run_dir_global)   
    
    if save_files == True: #Python files
      py_files = glob.glob('./**/*.py', recursive=True)
      ipynb_files = glob.glob('./**/*.ipynb', recursive=True)

      if not os.path.exists(run_dir_global+'/files/'):
        os.mkdir(run_dir_global+'/files/')

      for file in py_files:
        shutil.copy(file, run_dir_global+'/files/')

      for file in ipynb_files:
        shutil.copy(file, run_dir_global+'/files/')

      init_dict = {"python_files":run_dir_global+'/files/', 'sweep': sweep,'sweep_name': sweep_name}
      config_dict.update(init_dict)

    #config_dict.update(dataset_dict)
    
    data = {'run_id' : run_id_global, 'config_dict': str(dataset_dict), 'node_name': "Datasets", 'username': username, 'key': key}

    response = requests.post(protocol+'://'+IP+'/api/add_data', data=data)
  
          
    

def csv(run_id, dataframe, node_name="CSV"):
    columns_list = dataframe.columns.values.tolist()
    isnull_list = dataframe.isnull().sum().values.tolist()
    isunique_list = dataframe.nunique().values.tolist()
    size = sys.getsizeof(dataframe)/1024
    shape = dataframe.shape
    dtypes_list = []

    for d in dataframe.dtypes:
        dtypes_list.append(str(d))

    data = {'run_id': run_id, 'columns_list': str(columns_list), 'isnull_list': str(isnull_list),
            'isunique_list': str(isunique_list), 'dtypes_list': str(dtypes_list),
            'username': username, 'size': int(size), 'shape': str(shape), 'key': key, 'node_name': node_name}

    response = requests.post(protocol+'://'+IP+'/api/add_csv', data=data)

    if response.text == '0':
      print("Authentication failed")
    else:
      print("CSV Information saved.")


def evenly_spaced_points(fpr, tpr, N):
    if N <= 0:
        return []

    if N == 1:
        return [fpr[np.argmin(fpr)]]

    step_size = (len(fpr) - 1) / (N - 1)

    indices = [int(round(i * step_size)) for i in range(N)]

    selected_points_fpr = [fpr[i] for i in indices]
    selected_points_tpr = [tpr[i] for i in indices]
    
    return selected_points_fpr, selected_points_tpr

    

def specificity(y_true, y_pred):
    y_correct = np.isnan(np.divide(y_pred, y_true)) #0/0 -> nan, 1/0 -> inf
    y_correct = np.sum(y_correct)
    y_truth = np.count_nonzero(y_true == 0)
   
    return float(y_correct/y_truth)

def npv(y_true, y_pred): #Negative Predicted Value
    y_correct = np.isnan(np.divide(y_pred, y_true)) #0/0 -> nan, 1/0 -> inf
    y_correct = np.sum(y_correct)
    y_predicted = np.count_nonzero(y_pred == 0)
   
    return float(y_correct/y_predicted)

def get_roc_auc(y_true, y_pred):
    fpr, tpr, threshold = metrics.roc_curve(y_true, y_pred)
    roc_auc = metrics.auc(fpr, tpr)
    gmeans = np.sqrt(tpr * (1 - fpr)) #sensitivity * specificity (element-wise)
    index = np.argmax(gmeans) #Returns index of max value
    best_threshold = threshold[index]
   
    return fpr, tpr, roc_auc, gmeans, best_threshold, index

def get_metrics(y_true, y_pred, threshold):
    y_pred_binary = (y_pred > threshold).astype('float')
   
    prec = metrics.precision_score(y_true, y_pred_binary)
    rec = metrics.recall_score(y_true, y_pred_binary)
    spec = specificity(y_true, y_pred_binary)
    f1 = metrics.f1_score(y_true, y_pred_binary)
    acc = metrics.accuracy_score(y_true, y_pred_binary)
    npv_val = npv(y_true, y_pred_binary)
   
    c_matrix = metrics.confusion_matrix(y_true, y_pred_binary, labels=[0,1])

    c_matrix = c_matrix.tolist()

    c_matrix = [item for sublist in c_matrix for item in sublist]
   
    return prec, rec, spec, f1, acc, npv_val, c_matrix



# Create histogram here


'''
def save_torch_model(run_id, model):
    if not os.path.exists('mynacode'):
      os.mkdir('mynacode')
      
    with open('mynacode/'+str(run_id)+'/saved_network.pkl', 'wb') as f:
        dill.dump(model, f)

    torch.save(model.state_dict(), 'mynacode/'+str(run_id)+'/saved_state_dict.pt')
        
    files = {'network': open('mynacode/'+str(run_id)+'/saved_network.pkl','rb'), 'state_dict': open('mynacode/'+str(run_id)+'/saved_state_dict.pt','rb')}
    
    response = requests.post(protocol+'://'+IP+'/api/upload_pytorch_weights', files=files, data={'run_id':run_id, 'username': username, 'key': key})


def load_torch_model(run_id):

    response = requests.post(protocol+'://'+IP+'/api/get_pytorch_weights', data={'run_id':run_id, 'username': username, 'key': key})
    response = response.json()

    if not os.path.exists('mynacode'):
      os.mkdir('mynacode')

    if not os.path.exists('mynacode/'+str(run_id)):
      os.mkdir('mynacode/'+str(run_id))

    urllib.request.urlretrieve(response['weights'], 'mynacode/'+str(run_id)+'/'+response['weights'].split('/')[-1])
    urllib.request.urlretrieve(response['network'], 'mynacode/'+str(run_id)+'/'+response['network'].split('/')[-1])

    with open('mynacode/'+str(run_id)+'/saved_network.pkl', 'rb') as f:
        net = dill.load(f)


    net.load_state_dict(torch.load('mynacode/'+str(run_id)+'/saved_state_dict.pt'))

    return net
'''

def save_file(run_id, filepath):
    if not os.path.exists(filepath):
      print(filepath, ' doesn not exist')
      return 
        
    file = {'file': open(filepath,'rb')}
    
    response = requests.post(protocol+'://'+IP+'/api/upload_file', files=file, data={'run_id':run_id, 'username': username, 'key': key})


def config(config_dict = {}, node_name="Datasets", run_id = None, track=False):

  if track == True:
      global track_config
      track_config = config_dict
  else:
      if run_dir_global == "":
        print("Please run mynacode.start(...) before calling this function")
        return
      
      if not run_id:
        run_id = run_id_global

      if config_dict:
        file=open(run_dir_global+"/config.yaml","w")
        yaml.dump(config_dict,file)
        file.close()
        config_dict.update({'config_file': run_dir_global+"/config.yaml"})

      data = {'run_id' : run_id, 'config_dict': str(config_dict), 'node_name': node_name, 'username': username, 'key': key}
      
      response = requests.post(protocol+'://'+IP+'/api/add_data', data=data)      

    
def torch_model(model=None, metric_name=None, metric_value=None, goal='maximize', current_epoch=None, run_id=None):
    global prev_min
    global prev_max
    global metric_values
    global index_count
    global model_global
    global save_best_results
    global results_dict

    if run_dir_global == "":
      print("Please run mynacode.start(...) before calling this function")
      return

    if not os.path.exists(run_dir_global+'/model'):
      os.mkdir(run_dir_global+'/model')

    if model:
      with open(run_dir_global+'/model/saved_network.pkl', 'wb') as f:
          dill.dump(model, f)
          
      if goal == 'maximize':
        if metric_value > prev_max:
          prev_max = metric_value
          results_dict.update({'metric_name': metric_name})
          results_dict.update({'metric_goal': 'maximize'})
          results_dict.update({'best_'+metric_name: metric_value})
          results_dict.update({'best_metric_index': index_count})
          results_dict.update({'best_'+metric_name+'_epoch': current_epoch+1})
          
          model_global = model
          save_best_results = True
                      
      elif goal == 'minimize':
        if metric_value < prev_min:
          prev_min = metric_value
          results_dict.update({'metric_name': metric_name})
          results_dict.update({'metric_goal': 'minimize'})
          results_dict.update({'best_'+metric_name: metric_value})
          results_dict.update({'best_metric_index': index_count})
          results_dict.update({'best_'+metric_name+'_epoch': current_epoch+1})
          
          model_global = model
          save_best_results = True
          

      metric_values.append(metric_value)
      index_count += 1
    else:
      print("Please specify a Pytorch model.")
      return

def torch_save_best():

    global save_best_results
    global metric_values
    global index_count
    global model_global
    global results_dict

    if save_best_results == True:
      
      torch.save(model_global.state_dict(), run_dir_global+'/model/best_model_chkpt.pt')

      with open(run_dir_global+'/model/best_model_logs.txt', 'w') as f:
        f.write('Validation Metric: '+ str(results_dict['val_metric_name']))
        f.write('\nBest Value: ' + str(results_dict['best_val_'+results_dict['val_metric_name']]))
        f.write('\nBest Epoch: ' + str(results_dict['best_val_epoch']))
        
      model_dict = {'metric_values': metric_values,
                          'best_model_path': run_dir_global+'/model/best_model_chkpt.pt',
                          'best_model_logs': run_dir_global+'/model/best_model_logs.txt'}

      config_dict = {**model_dict, **results_dict, **track_config}
      
      results(results_dict = config_dict, run_id = None, node_name = 'Results')
      
    save_best_results = False
    index_count = 0
    metric_values = []
    model_global = None
    results_dict = {}


def newest(path):
    files = os.listdir(path)
    print(path)
    print(files)
    if len(files) == 0:
        return None
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime)
    

def data(train_set=[], train_labels=[], test_set=[], test_labels=[], val_set=[], val_labels=[], dataset_name="", #checks if data is same as prev
         problem_type = 'binary classification',  node_name="Datasets", if_sweep_save_once = True, run_id = None):


  #global dataset_dict
  if if_sweep_save_once == True and first_sweep_run == True:
    print("Dataset saved on first run. Subsequent calls to the 'data()' function within the current sweep will be ignored.")
    return
  
  config_dict = {}
  
  train_set = np.array(train_set)
  val_set = np.array(val_set)
  test_set = np.array(test_set)

  train_labels = np.array(train_labels)
  val_labels = np.array(val_labels)
  test_labels = np.array(test_labels)

  if project_dir_global == "":
    print("Please run mynacode.start(...) before calling this function")
    return
  current_dir = project_dir_global
 

  if not os.path.exists(current_dir+'/data'):
    os.mkdir(current_dir+'/data')

  if len(str(dataset_name)) == 0:
      dataset_name = 'dataset'

  # Check latest dataset folder
  save_new_data_flag = 0
  newest_data_folder = newest(current_dir+'/data')
  print("Latest:", newest_data_folder)

  if newest_data_folder == None:
      save_new_data_flag = 1
  elif re.split(r'[\\/]', newest_data_folder)[-1].split('_')[0] != dataset_name:
      save_new_data_flag = 1
  else:
      if (len(train_labels) > 0) and (os.path.exists(newest_data_folder + '/train_labels.pkl')): #Both exist
          percent_20 = int((20/100)*len(train_labels))
          
          with open(newest_data_folder + '/train_labels.pkl', 'rb') as f:
              x = dill.load(f)

              if not np.array_equal(x[:percent_20], train_labels[:percent_20]): #Both exist but not equal
                  save_new_data_flag = 1
      elif (~(os.path.exists(newest_data_folder + '/train_labels.pkl'))) and (len(train_labels) == 0): #Both don't exist
          pass
      else: #One exists, one doesn't
          save_new_data_flag = 1
              
      if ((os.path.exists(newest_data_folder + '/val_labels.pkl')) and (save_new_data_flag == 0) and (len(val_labels) > 0)):
          percent_20 = int((20/100)*len(val_labels))

          with open(newest_data_folder + '/val_labels.pkl', 'rb') as f:
              x = dill.load(f)

              if not np.array_equal(x[:percent_20], val_labels[:percent_20]):
                  save_new_data_flag = 1
      elif ((~(os.path.exists(newest_data_folder + '/val_labels.pkl'))) and (save_new_data_flag == 0) and (len(val_labels) == 0)):
          pass  
      else:
          save_new_data_flag = 1


      if (os.path.exists(newest_data_folder + '/test_labels.pkl')) and (save_new_data_flag == 0) and (len(test_labels) > 0):
          percent_20 = int((20/100)*len(test_labels))

          with open(newest_data_folder + '/test_labels.pkl', 'rb') as f:
              x = dill.load(f)
              
              if not np.array_equal(x[:percent_20], test_labels[:percent_20]):
                  save_new_data_flag = 1
      elif ((~(os.path.exists(newest_data_folder + '/test_labels.pkl'))) and (save_new_data_flag == 0) and (len(test_labels) == 0)):
          pass
      else:
          save_new_data_flag = 1
            
  if save_new_data_flag == 1:
      
      while os.path.exists(current_dir+'/data/'+dataset_name):
          dataset_name = dataset_name+"_" + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6))
          
      os.mkdir(current_dir+'/data/'+dataset_name)
        
      if len(train_set) > 0:
        with open(current_dir+'/data/'+dataset_name+'/train_set.pkl', 'wb') as f:
            dill.dump(train_set, f)
        config_dict.update({'train_set': current_dir+'/data/'+dataset_name+'/train_set.pkl'})

      if len(val_set) > 0:
        with open(current_dir+'/data/'+dataset_name+'/val_set.pkl', 'wb') as f:
            dill.dump(val_set, f)
        config_dict.update({'val_set': current_dir+'/data/'+dataset_name+'/val_set.pkl'})

      if len(test_set) > 0:
        with open(current_dir+'/data/'+dataset_name+'/test_set.pkl', 'wb') as f:
            dill.dump(test_set, f)
        config_dict.update({'test_set': current_dir+'/data/'+dataset_name+'/test_set.pkl'})


      if len(train_labels) > 0:
        train_unique, train_count = np.unique(train_labels, return_counts=True)
        config_dict.update({'labels_train': train_unique.tolist(), 'train_count':train_count.tolist()})
        with open(current_dir+'/data/'+dataset_name+'/train_labels.pkl', 'wb') as f:
            dill.dump(train_labels, f)

      if len(val_labels) > 0:
        val_unique, val_count = np.unique(val_labels, return_counts=True)
        config_dict.update({'labels_val': val_unique.tolist(), 'val_count':val_count.tolist()})
        with open(current_dir+'/data/'+dataset_name+'/val_labels.pkl', 'wb') as f:
            dill.dump(val_labels, f)

      if len(test_labels) > 0:
        test_unique, test_count = np.unique(test_labels, return_counts=True)
        config_dict.update({'labels_test': test_unique.tolist(), 'test_count':test_count.tolist()})
        with open(current_dir+'/data/'+dataset_name+'/test_labels.pkl', 'wb') as f:
            dill.dump(test_labels, f)

      config_dict.update({'prev_saved_data': False})
  else:
      print("Datasets have already been saved previously.")
      config_dict.update({'prev_saved_data': True})


  data = {'run_id' : run_id_global, 'config_dict': str(config_dict), 'node_name': "Datasets", 'username': username, 'key': key}

  response = requests.post(protocol+'://'+IP+'/api/add_data', data=data)       

  #dataset_dict = config_dict
      


def torch_data(train_dataloader=None, val_dataloader=None, test_dataloader=None, dataset_name="", label_index=1,
         problem_type = 'binary classification',  node_name="Datasets", if_sweep_save_once = True, run_id = None):

  #global dataset_dict
  global first_sweep_run
  
  if (if_sweep_save_once == True) and (first_sweep_run == False) and (sweep_global == True):
    print("Dataset saved on first run. Subsequent calls to the 'data()' function within the current sweep will be ignored.")
    return

  config_dict = {}

  if project_dir_global == "":
    print("Please run mynacode.start(...) before calling this function")
    return
  current_dir = project_dir_global

  if not os.path.exists(current_dir+'/data'):
    os.mkdir(current_dir+'/data')

  if len(str(dataset_name)) == 0:
      dataset_name = 'dataset'

  # Check latest dataset folder
  save_new_data_flag = 0
  newest_data_folder = newest(current_dir+'/data')
  print("Latest Dataset Folder: ", newest_data_folder)

  if newest_data_folder == None:
      print("a")
      save_new_data_flag = 1
  elif re.split(r'[\\/]', newest_data_folder)[-1].split('_')[0] != dataset_name:
      print("b")
      save_new_data_flag = 1
  else:
      if (train_dataloader != None) and (len(train_dataloader) > 0) and (os.path.exists(newest_data_folder + '/train_dataloader.pkl')): #Both exist
          print("c")
          
          with open(newest_data_folder + '/train_dataloader.pkl', 'rb') as f:
              x = dill.load(f)
              torch.manual_seed(0)
              b1 = next(iter(train_dataloader))[label_index]
              torch.manual_seed(0)
              b2 = next(iter(x))[label_index]

              if not np.array_equal(b1, b2):
                  print(b1, b2)
                  save_new_data_flag = 1
      elif (~(os.path.exists(newest_data_folder + '/train_dataloader.pkl'))) and (train_dataloader == None): #Both don't exist
          print("d")
          pass
      else: #One exists, one doesn't
          print("e")
          save_new_data_flag = 1
              
      if ((os.path.exists(newest_data_folder + '/val_dataloader.pkl')) and (save_new_data_flag == 0) and (val_dataloader != None) and (len(val_dataloader) > 0)):
          print("f")
          with open(newest_data_folder + '/val_dataloader.pkl', 'rb') as f:
              x = dill.load(f)
              torch.manual_seed(0)
              b1 = next(iter(val_dataloader))[label_index]
              torch.manual_seed(0)
              b2 = next(iter(x))[label_index]

              if not np.array_equal(b1, b2):
                  print(b1, b2)
                  save_new_data_flag = 1
      elif ((~(os.path.exists(newest_data_folder + '/val_dataloader.pkl'))) and (save_new_data_flag == 0) and (val_dataloader == None)):
          print("g")
          pass  
      else:
          print("h")
          save_new_data_flag = 1


      if (os.path.exists(newest_data_folder + '/test_dataloader.pkl')) and (save_new_data_flag == 0) and (test_dataloader != None) and (len(test_dataloader) > 0):
          print("i")
          with open(newest_data_folder + '/test_dataloader.pkl', 'rb') as f:
              x = dill.load(f)
              torch.manual_seed(0)
              b1 = next(iter(test_dataloader))[label_index]
              torch.manual_seed(0)
              b2 = next(iter(x))[label_index]
              
              if not np.array_equal(b1, b2):
                  print(b1, b2)
                  save_new_data_flag = 1
      elif ((~(os.path.exists(newest_data_folder + '/test_dataloader.pkl'))) and (save_new_data_flag == 0) and (test_dataloader == None)):
          print("j")
          pass
      else:
          print("k")
          save_new_data_flag = 1

  if save_new_data_flag == 1:
      print("l")
      
      while os.path.exists(current_dir+'/data/'+dataset_name):
          dataset_name = dataset_name+"_" + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6))
          
      os.mkdir(current_dir+'/data/'+dataset_name)

      if train_dataloader:
        #if label_index:
          #train_labels = [np.array(train_dataloader.dataset[i][label_index]) for i in range(len(train_dataloader.dataset))]
        with open(current_dir+'/data/'+dataset_name+'/train_dataloader.pkl', 'wb') as f:
            dill.dump(train_dataloader, f)
        config_dict.update({'train_dataloader': current_dir+'/data/'+dataset_name+'/train_dataloader.pkl'})

      if val_dataloader:
        #if label_index:
          #val_labels = [np.array(val_dataloader.dataset[i][label_index]) for i in range(len(val_dataloader.dataset))]
        with open(current_dir+'/data/'+dataset_name+'/val_dataloader.pkl', 'wb') as f:
            dill.dump(val_dataloader, f)
        config_dict.update({'val_dataloader': current_dir+'/data/'+dataset_name+'/val_dataloader.pkl'})

      if test_dataloader:
        #if label_index:
          #test_labels = [np.array(test_dataloader.dataset[i][label_index]) for i in range(len(test_dataloader.dataset))]
        with open(current_dir+'/data/'+dataset_name+'/test_dataloader.pkl', 'wb') as f:
            dill.dump(test_dataloader, f)
        config_dict.update({'test_dataloader': current_dir+'/data/'+dataset_name+'/test_dataloader.pkl'})


      '''
      train_labels = np.array(train_labels)
      val_labels = np.array(val_labels)
      test_labels = np.array(test_labels)
        
      if len(train_labels) > 0:
        train_unique, train_count = np.unique(train_labels, return_counts=True)
        config_dict.update({'train_labels': train_unique.tolist(), 'train_count':train_count.tolist()})

      if len(val_labels) > 0:
        val_unique, val_count = np.unique(val_labels, return_counts=True)
        config_dict.update({'val_labels': val_unique.tolist(), 'val_count':val_count.tolist()})

      if len(test_labels) > 0:
        test_unique, test_count = np.unique(test_labels, return_counts=True)
        config_dict.update({'test_labels': test_unique.tolist(), 'test_count':test_count.tolist()})
      '''
        
      config_dict.update({'prev_saved_data': False})
  else:
      print("Datasets have already been saved previously.")
      config_dict.update({'prev_saved_data': True})

  if (first_sweep_run == True) and (sweep_global == True):
    first_sweep_run = False

  data = {'run_id' : run_id_global, 'config_dict': str(config_dict), 'node_name': "Datasets", 'username': username, 'key': key}

  response = requests.post(protocol+'://'+IP+'/api/add_data', data=data) 
  #dataset_dict = config_dict



try:
  class MynacodeCallback(keras.callbacks.Callback):

      def __init__(self, metric_name, goal='maximize', run_id=None):                                                                                                                                                                                                             
          self.metric_name = metric_name                                                                                                                                                                                                                                            
          self.goal = goal                                                                                                                                                                                                                                      
          self.run_id = run_id
          self.best_model = None
          self.best_metric_value = 0
          self.best_metric_epoch = 0
          self.save_model = False

          if run_dir_global == "":
            print("Please run mynacode.start(...) before calling this function")
            return


      def on_train_end(self, logs=None):

          global save_best_results
          global metric_values
          global index_count
          global model_global
          global results_dict

          if save_best_results == True:
            if not os.path.exists(run_dir_global+'/model'):
              os.mkdir(run_dir_global+'/model')

            model_global.save(run_dir_global+'/model/best_model_chkpt.hdf5')

            with open(run_dir_global+'/model/best_model_logs.txt', 'w') as f:
              f.write('Validation Metric: '+ str(results_dict['val_metric_name']))
              f.write('\nBest Value: ' + str(results_dict['best_val_'+results_dict['val_metric_name']]))
              f.write('\nBest Epoch: ' + str(results_dict['best_val_epoch']))


            model_dict = {'metric_values': metric_values,
                                'best_model_path': run_dir_global+'/model/best_model_chkpt.hdf5',
                                'best_model_logs': run_dir_global+'/model/best_model_logs.txt'}

            config_dict = {**model_dict, **results_dict, **track_config}
            
            results(results_dict = config_dict, run_id = None, node_name = 'Results')

          save_best_results = False
          index_count = 0
          metric_values = []
          model_global = None
          results_dict = {}


      def on_epoch_end(self, epoch, logs=None):
          global metric_values
          global index_count
          global prev_min
          global prev_max
          global results_dict
          global save_best_results
          global model_global
          

          if self.metric_name not in logs.keys():
            print(self.metric_name + ' not found in log keys')
            keys = list(logs.keys())
            print("End epoch {} of training; got log keys: {}".format(epoch, keys))
          else: 
            if self.goal == 'maximize':
              if logs.get(self.metric_name) > prev_max:
                prev_max = logs.get(self.metric_name)
                results_dict.update({'metric_name': self.metric_name})
                results_dict.update({'metric_goal': 'maximize'})
                results_dict.update({'best_'+self.metric_name: logs.get(self.metric_name)})
                results_dict.update({'best_metric_index': index_count})
                results_dict.update({'best_'+self.metric_name+'_epoch': epoch+1})
                
                model_global = self.model
                save_best_results = True
                            
            elif self.goal == 'minimize':
              if logs.get(self.metric_name) < prev_min:
                prev_min = logs.get(self.metric_name)
                results_dict.update({'metric_name': self.metric_name})
                results_dict.update({'metric_goal': 'minimize'})
                results_dict.update({'best_'+self.metric_name: logs.get(self.metric_name)})
                results_dict.update({'best_metric_index': index_count})
                results_dict.update({'best_'+self.metric_name+'_epoch': epoch+1})
                
                model_global = self.model
                save_best_results = True
                

            metric_values.append(logs.get(self.metric_name))
            index_count += 1
except:
  pass





def results(y_true = [], y_predicted = [], threshold=0.5, results_dict = {}, node_name="Results", problem_type = 'binary classification', run_id = None):

    if not run_id:
      run_id = run_id_global
    
    if len(y_true) != 0 and len(y_predicted) != 0:
      
      y_predicted = np.array(y_predicted).flatten()
      y_true = np.array(y_true).flatten()

      zero_idx = np.where(y_true == 0)[0]
      one_idx = np.where(y_true == 1)[0]
      
      prec, rec, spec, f1, acc, npv_val, c_matrix = get_metrics(y_true, y_predicted, threshold)
      fpr, tpr, roc_auc, gmeans, best_threshold, index = get_roc_auc(y_true, y_predicted)

      fpr_spaced, tpr_spaced = evenly_spaced_points(fpr, tpr, 500)

      hist_zero = plt.hist(y_predicted[zero_idx].tolist(), bins=30)
      hist_zero_freq = hist_zero[0]
      hist_zero_bins = hist_zero[1]
      
      hist_one = plt.hist(y_predicted[one_idx].tolist(), bins=30)
      hist_one_freq = hist_one[0]
      hist_one_bins = hist_one[1]

      binary = {'precision': round(prec, 4), 'recall': round(rec, 4), 'specificity': round(spec, 4),
              'f1': round(f1, 4), 'accuracy': round(acc, 4), 'npv': round(npv_val, 4), 'c_matrix': c_matrix,
              'test_auc': roc_auc, 'hist_zero_freq': hist_zero_freq.tolist(), 'hist_zero_bins': hist_zero_bins.tolist(),
              'hist_one_freq': hist_one_freq.tolist(), 'hist_one_bins': hist_one_bins.tolist(),'fpr': fpr_spaced, 'tpr': tpr_spaced,
              'threshold': round(threshold, 4)}

      results_dict.update(binary)

    data = {'run_id' : run_id, 'results_dict': str(results_dict), 'node_name': node_name, 'username': username, 'key': key}

    response = requests.post(protocol+'://'+IP+'/api/add_results', data=data)
  
    if response.text == '0':
      print("Authentication failed")
    else:
      print("Results saved")
