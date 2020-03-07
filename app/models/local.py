from datetime import datetime

class LocalModel:
    dataStore = dict()

def create_execution(run_id):
    LocalModel.dataStore.update({run_id: {
        'key': {"name": run_id},
        'status': 'scheduled',
        'scheduled': datetime.now(),
        'modified': datetime.now()
        }
    })


def update_execution(run_id, status):
    print(f"Updating execution {run_id}")
    currentDict = LocalModel.dataStore.get(run_id)
    currentDict.update(status = status)
    currentDict.update(modified = datetime.now())
    LocalModel.dataStore.update({run_id: currentDict})


def add_storage_link(run_id, link_name, link_url):
    print(f"Adding storage link {link_name} to run {run_id}")
    currentDict = LocalModel.dataStore.get(run_id)
    currentDict.update({link_name: link_url})
    LocalModel.dataStore.update({run_id: currentDict})

def get_executions():
    return list(LocalModel.dataStore.values())