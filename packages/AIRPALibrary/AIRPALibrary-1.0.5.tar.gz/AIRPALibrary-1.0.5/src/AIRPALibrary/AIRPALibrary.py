import json
import os
import requests
from subprocess import check_output, Popen, PIPE
import signal
import getpass


class AIRPALibrary:
    def __init__(self):
        self.proses = True
        self.runner = None
        self.message = 'True'
        pass
    
    def start_timeout(self, seconds='10', process_name='IEDriverServer.exe'):
        '''Fungsi untuk menjalankan timeout dengan input yaitu berapa lama timeout akan dilakukan, serta
        proses apa yang ingin dimatikan
        
        Contoh penggunaan :

            Start Timeout    10    excel.exe
            Run Keyword And Ignore Error    Open Macro
            End Timeout
        '''
        self.initiate_timeout(True)
        self.timeout_process(seconds,process_name)
        
    def end_timeout(self):
        '''Fungsi untuk mendapatkan keterangan dari timeout yang dilakukan apakah berhasil atau tidaknyanya proses
        dijalankan dalam kurun waktu tertentu'''
        self.initiate_timeout(False)
        self.get_timeout_info()
    
    def get_timeout_info(self):
        if self.proses :
            if self.runner.communicate()[0].strip().decode('utf-8')[-5:].strip()=='True':
                raise RuntimeError('The execution failed because of time exceeded')
            else :
                print('Execution sucessfully initiated')
        else :
            if self.message=='True' :
                raise RuntimeError('The execution failed because of time exceeded')
            else :
                print('Execution sucessfully initiated')
    
    def initiate_timeout(self, set=True):
        if set:
            self.proses = set
        else :
            self.proses = set
            try :
                value = Popen("Taskkill /F /T /PID %d " % self.runner.pid+' /FI "USERNAME eq '+getpass.getuser(), stdout=PIPE)
                value = value.communicate()[0].strip().decode('utf-8').strip()
                if value!='INFO: No tasks running with the specified criteria.':
                    self.message = 'False'
            except :
                pass
                    
    def kill_process(self, process_name='excel.exe'):
        os.system('taskkill /F /IM '+process_name+' /FI "USERNAME eq '+getpass.getuser())
    
    def read_config(self,additional=None):
        ''' fungsi untuk membaca file konfigurasi json, pengguna dapat menambahkan untuk data 
            yang dibutuhkan dengan format json object. Output dari fungsi ini adalah file konfigurasi
            dalam bentuk json object.
            
            contoh penggunaan :
                ${config}=  read_config
            
        '''
        try:
            with open(os.getcwd()+'\\config.json') as jsonfile:
                conf = json.load(jsonfile)
        except:
            raise RuntimeError('File config.json tidak ditemukan')
        
        if additional!=None:
            try:
                conf.update(json.loads(additional))
            except:
                raise RuntimeError('Pastikan kembali json object yang dimasukkan sebagai parameter')
        return conf
    
    def timeout_process(self, seconds='10', process_name='IEDriverServer.exe'):
        if self.proses :
            self.runner = Popen(["python", os.path.dirname(os.path.realpath(__file__))+'\\function_timeout_robot.py',seconds,process_name], stdout=PIPE)
        else :
            value = Popen("Taskkill /F /T /PID %d " % self.runner.pid+' /FI "USERNAME eq '+getpass.getuser(), stdout=PIPE)
            value = value.communicate()[0].strip().decode('utf-8').strip()
            self.message = (value!='INFO: No tasks running with the specified criteria.')
            
    
    def timeout(self, function_module=None, seconds='10', process_name='excel.exe'):
        ''' Fungsi untuk menjalankan fungsi pada module dengan tambahan waktu timeout, fungsi ini memiliki parameter default kill process "excel.exe" dan timeout selama 10 detik
            
            Contoh Penggunaan :
                Timeout     [module].[fungsi]\n
                Timeout     [module].[fungsi]   30\n
                Timeout     [module].[fungsi]   30      apps.exe\n
                '''
        if function_module==None:
            raise RuntimeError('Please specify the module that need to be executed')
        
        value = check_output(["python", os.path.dirname(os.path.realpath(__file__))+'\\function_timeout.py',seconds,function_module,process_name])
        
        if bool(value.strip()[-5:].decode('utf-8'))==True:
            raise RuntimeError('The execution failed because of time exceeded')
        else :
            print('Execution sucessfully initiated')
            
    def get_id_sharepoint(self, path_url, hostname='astrainternational.sharepoint.com'):
        
        base_url = os.getenv("RPAEmailGateway")
        cli_code = os.getenv("RPAEmailGatewayCode")
        
        try:
            url = base_url+"/get_sites_sharepoint"
            headers = {
                'X-Client-Code': cli_code
            }
            payload={
                'hostname': hostname,
                'path_url': path_url
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.text)
            item = response.json()
            return item, True
        except Exception as e:
            print("Message:\n", e)
            return '', False

    def get_list_site(self, site_id):
        
        base_url = os.getenv("RPAEmailGateway")
        cli_code = os.getenv("RPAEmailGatewayCode")
        
        try:
            url = base_url+"/get_drives"
            headers = {
                'X-Client-Code': cli_code
            }
            payload={
                    'site_id': site_id
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            item = response.json()
            return item["data"]
        except Exception as e:
            print("Message:", e)


    def get_list_file_drive(self, site_id, file_id):
        
        base_url = os.getenv("RPAEmailGateway")
        cli_code = os.getenv("RPAEmailGatewayCode")
        
        try:
            url = base_url+"/get_file_drives"
            headers = {
                'X-Client-Code': cli_code
            }
            payload={
                    'site_id': site_id,
                    'file_id': file_id
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            item = response.json()
            print('Response:', response.reason)
            return item["data"]
        except Exception as e:
            print("Message:", e)

    def loop_folder(self, site_id, list_file, lst_path):
        cur_path = ''
        for path in lst_path:
            cur_path = path
            for file in list_file:
                if file['name'] != path:
                    continue
                file_id = file['id']
                list_file = self.get_list_file_drive(site_id, file_id)
        if cur_path == lst_path[-1]:
            return list_file

    def get_files_folder(self, site_id, main_path):
        files_site = self.get_list_site(site_id)
        files = self.loop_folder(site_id, files_site, main_path)
        return files

    def download_file(self, site_id, file_id, name):
        
        base_url = os.getenv("RPAEmailGateway")
        cli_code = os.getenv("RPAEmailGatewayCode")
        
        try:
            url = base_url+"/get_files_sites"
            headers = {
                'X-Client-Code': cli_code
            }
            payload={
                    'file_id': file_id,
                    'site_id': site_id
            }
            r = requests.request("POST", url, headers=headers, data=payload)
            if r.status_code == 200:
                with open(name, 'wb') as f:
                    f.write(r.content)
                print(f"File successfully downloaded, saved: {str(name)}")
                return True
            else:
                print(f"Failed to download, code: {r.status_code}")
                return False
        except Exception as e:
            print(f"Failed to download, {e}")
            return False

    def get_worksheets(self, site_id, file_id):
        base_url = os.getenv("RPAEmailGateway")
        cli_code = os.getenv("RPAEmailGatewayCode")
        
        try:
            url = base_url+"/get_worksheets"
            headers = {
                'X-Client-Code': cli_code
            }
            payload={
                    'site_id': site_id,
                    'file_id': file_id
            }
            response = requests.post(url, headers=headers, data=payload)
            items = response.json()['data']
            shts_name = []
            for item in items:
                shts_name.append(item['name'])
            return shts_name
        except Exception as e:
            print("Message:", e)
            return []

    def write_excel(self, site_id, file_id, sheet, cell_range, tipe, data):
        
        base_url = os.getenv("RPAEmailGateway")
        cli_code = os.getenv("RPAEmailGatewayCode")
        
        try:
            url = base_url+"/insert_data"
            headers = {
                'X-Client-Code': cli_code
            }
            payload={
                    'site_id': site_id,
                    'file_id': file_id,
                    'sheet': sheet,
                    'range': cell_range,
                    "data": {
                        tipe: data
                    }
            }
            response = requests.post(url, headers=headers, json=payload)
            print(response.json()['data'])
        except Exception as e:
            print("Message:", e)

    def protection_ws(self, site_id, file_id, sht_nm, tipe):
        
        base_url = os.getenv("RPAEmailGateway")
        cli_code = os.getenv("RPAEmailGatewayCode")
        
        try:
            url = base_url+"/protection_ws"
            headers = {
                'X-Client-Code': cli_code
            }
            payload={
                    'site_id': site_id,
                    'file_id': file_id,
                    'sheet': sht_nm,
                    'tipe': tipe
            }
            response = requests.post(url, headers=headers, data=payload)
            print(str(tipe).capitalize()+", with code:", response.status_code)
        except Exception as e:
            print("Message:", e)

    def get_email(self, email, subject, limit=None, threshold=None, bodycontent=None, content=None):
        
        base_url = os.getenv("RPAEmailGateway")
        cli_code = os.getenv("RPAEmailGatewayCode")
        
        items = {}
        url = base_url+"/get_email"
        headers = {
            'X-Client-Code': cli_code
        }
        payload={
            'email': email,
            'subject': subject
        }
        if bodycontent is not None:
            payload['bodycontent'] = bodycontent
        if threshold is not None:
            payload['threshold'] = threshold
        if content is not None:
            payload['content'] = content
        if limit is not None:
            payload['limit'] = limit
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            items = response.json()
        except Exception as e:
            items = {"success":False, "data":e}
        return items

    def get_attachment(self, filename, email, email_id, att_id):
        
        base_url = os.getenv("RPAEmailGateway")
        cli_code = os.getenv("RPAEmailGatewayCode")
        
        url = base_url+"/get_attachment"
        try:
            payload={
                'email': email,
                'email_id': email_id,
                'attachment_id': att_id
            }
            headers = {
                'X-Client-Code': cli_code
            }
            fn = filename
            response = requests.request("POST", url, headers=headers, data=payload)
            with open(fn, "wb") as _file:
                _file.write(response.content)
            print("Attachment saved to " + str(fn))
        except Exception as e:
            print({"success":False, "message":e})

    def move_email(self,email, email_id, destination='Archive'):
        
        base_url = os.getenv("RPAEmailGateway")
        cli_code = os.getenv("RPAEmailGatewayCode")
        
        url = base_url + "/move_email"
        payload={
            'email': email,
            'email_id': email_id,
            'destination': destination
        }
        headers = {
            'X-Client-Code': cli_code
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        
    def create_upload_session(self, site_id, drive_id, item_id, file_path):
        print("Create...")
        
        base_url = os.getenv("RPAEmailGateway")
        cli_code = os.getenv("RPAEmailGatewayCode")
        
        try:
            url = base_url+"/create_upload_session"
            headers = {
                'X-Client-Code': cli_code
            }
            payload={
                    'site_id': site_id,
                    'drive_id': drive_id,
                    'item_id': item_id,
                    'file_path': file_path
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            item = response.json()
            print('Response:', response.text)
            return item['data']
        except Exception as e:
            print("Message:", e)

    def upload_file_sharepoint(self, filename, url_session):
        print("Filename:", filename)
        with open(filename, 'rb') as up:
            total_file_size = os.path.getsize(filename)
            chunk_size = 327680
            chunk_number = total_file_size//chunk_size
            chunk_leftover = total_file_size - (chunk_size * chunk_number)
            counter = 0
            while True:
                try:
                    chunk_data = up.read(chunk_size)
                    start_index = counter * chunk_size
                    end_index = start_index + chunk_size

                    if not chunk_data:
                        break
                    if counter == chunk_number:
                        end_index = start_index + chunk_leftover
                    headers = {
                        'Content-Length': f'{chunk_size}',
                        'Content-Range': f'bytes {start_index}-{end_index-1}/{total_file_size}'
                    }
                    res = requests.put(url=url_session, data=chunk_data, headers=headers)
                    print(f'Reason: {res.reason}, Status code: {res.status_code}')
                    if 'createdBy' in res.json():
                        res = res.json()
                        print(f'File {res["name"]} upload completed.')
                        print(f'at {res["parentReference"]["path"]}')
                    else:
                        print('Upload progress:', res.json()['nextExpectedRanges'])
                        counter += 1
                except Exception as e:
                    print('Upload Failed:', e)
    
    def send_email(self, subject=None, content=None, to=None, cc=None, file_path=None, sender=None):
        ''' Fungsi untuk mengirimkan email dengan parameter input sebagai berikut ini :\n
            subject = (string) masukkan subject yang anda inginkan, contoh : RPA Email\n
            content = (string) masukkan content email atau isi dari email. content email bisa juga dengan menggunakan html layouting\n
            Untuk masukkan data receiver email baik to maupun cc bisa tunggal(string or list) atau banyak(list). Contoh adalah sebagai berikut : \n
            tunggal :
                to = 'example@contoh.com'   atau    to = ['example@contoh.com']\n
                cc = 'example@contoh.com'   atau    cc = ['example@contoh.com']
            banyak :
                to = ['example1@contoh.com','example2@contoh.com']\n
                cc = ['example1@contoh.com','example2@contoh.com']
                
            Untuk masukkan file path harus menggunakan full path file dan bisa tunggal(string or list) atau banyak(list). Contoh adalah sebagai berikut : \n
            tunggal :
                file_path = 'C://Dir//filename.exentension'   atau    file_path = ['C://Dir//filename.exentension']
            banyak :
                file_path = ['C://Dir//filename1.exentension','C://Dir//filename2.exentension']
                
            Contoh penggunaan dalam robot framework :
                Send Email    Isi Subject    Isi Content Message    example@contoh.com    ${None}    C:\\Doc\\filename.xls\n
                Send Email    Isi Subject    Isi Content Message    ${list_email}    ${None}    C:\\Doc\\filename.xls\n
                Send Email    Isi Subject    Isi Content Message    ${list_email}    ${None}    ${full_path_file_list}    
            '''
        base_url = os.getenv("RPAEmailGateway")
        cli_code = os.getenv("RPAEmailGatewayCode")
        url = base_url+"/send_email"
        
        if subject==None or content==None or to==None:
            raise RuntimeError('Subject, content and receiver email must not be empty')
        
        if isinstance(to, list)==False : to = [to]
        
        payload={
                'to':';'.join(to),
                'subject': subject,
                'content': content}
        
        if cc!=None:
            if isinstance(cc, list)==False : cc = [cc]
            payload['cc'] = ';'.join(str(c) for c in cc)
            
        if sender!=None:
            payload['from'] = sender
        
        headers = {
            'X-Client-Code':cli_code
        } 
        
        try:
            if file_path!=None:
                files = {}
                
                if isinstance(file_path, list)==False : file_path = [file_path]
            
                for i in range(len(file_path)):
                    index_file=f'file{i}:'
                    read_file=open(file_path[i], 'rb')
                    files[index_file] = read_file
                    
                response = requests.request("POST", url, headers=headers, data=payload, files=files)
            else :
                response = requests.request("POST", url, headers=headers, data=payload)  
            
            if 'error' in response.text:
                raise RuntimeError(response.text)
            else :
                print(response.text)
        except Exception as e:
            raise RuntimeError(e)
        
        
    