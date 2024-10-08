from fastapi import FastAPI, APIRouter, Depends
from bs4 import BeautifulSoup
import requests
from .. import oauth2


router = APIRouter(
    tags=['API'],
    
)


@router.get("/producao", summary="Dados de produção", description="Carrega dados de produção de vinhos, sucos e derivados do Rio Grande do Sul")
def load_prod(limit: int = 10, skip: int = 0, search: str = "", current_user: dict = Depends(oauth2.get_current_active_user) ):
    all_data = {}
    for i in range(1970, 2024, 1):
        url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={i}&opcao=opt_02"
        try:
            page = requests.get(url)
            page.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching data for year {i}: {e}")
            continue  # Skip this year if there's an error
        
        soup = BeautifulSoup(page.text, 'html.parser')

        table = soup.find("table", class_="tb_base tb_dados")
            
        column_data = table.find_all('tr')

        year_data = []
        for row in column_data[1:]:
            row_data = row.find_all('td')

            if len(row_data) > 1:
                first_column_data = row_data[0].text.strip()
                second_column_data = row_data[1].text.strip()
                if search and search.lower() not in (first_column_data.lower(), second_column_data.lower()):
                    continue
                year_data.append({
                    "Produto": first_column_data, 
                    "Valor": second_column_data
                    })
        all_data[i] = year_data[skip:skip + limit]


    return all_data

@router.get("/processamento",summary="Dados de processamento", description="Carrega dados de quantidade de uvas processadas no Rio Grande do Sul")
def load_process(limit: int = 10, skip: int = 0, search: str = "" , current_user: dict = Depends(oauth2.get_current_active_user)):
    subopcao_mapping = {
        'subopt_01': 'Viniferas',
        'subopt_02': 'Americanas e Híbridas',
        'subopt_03': 'Uvas de Mesa',
        'subopt_04': 'Sem Classificação',
    }
    subopcao = ['subopt_01', 'subopt_02','subopt_03','subopt_04'] 
    all_data = {}
    for sub in subopcao:
        sub_data = {}
        for i in range(1970, 2024, 1):
            url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={i}&opcao=opt_03&subopcao={sub}"
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            
            table = soup.find("table", class_="tb_base tb_dados")

            tbody = table.find('tbody')

            rows = tbody.find_all('tr')

            year_data = []
            for row in rows:
                row_data = row.find_all('td')
                if len(row_data) > 1:
                    first_column_data = row_data[0].text.strip()
                    second_column_data = row_data[1].text.strip()
                    year_data.append({
                        "Cultivar": first_column_data, 
                        "Quantidade Kg" : second_column_data
                        })
      
            sub_data[i] = year_data[skip:skip + limit]

        all_data[subopcao_mapping[sub]] = sub_data
    
    return all_data




@router.get("/comercializacao",summary="Dados de comercialização", description="Carrega dados de comercialização de vinhos e derivados no Rio Grande do Sul.")
def load_com(limit: int = 10, skip: int = 0, search: str = "", current_user: dict = Depends(oauth2.get_current_active_user) ):
    all_data = {}
    for i in range(1970, 2024, 1):
        url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={i}&opcao=opt_04"
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        table = soup.find("table", class_="tb_base tb_dados")
        
        column_data = table.find_all('tr')

        year_data = []
        for row in column_data[1:]:
            row_data = row.find_all('td')

            if len(row_data) > 1:
                first_column_data = row_data[0].text.strip()
                second_column_data = row_data[1].text.strip()
                if search and search.lower() not in first_column_data.lower():
                    continue
                year_data.append({
                    "Produto": first_column_data, 
                    "Valor": second_column_data
                    })
        all_data[i] = year_data[skip:skip + limit]

    return all_data



@router.get("/importacao",summary="Dados de importação", description="Carrega dados de importação de derivados de uva.")
def load_import(limit: int = 10, skip: int = 0, search: str = "", current_user: dict = Depends(oauth2.get_current_active_user) ):
    subopcao_mapping = {
        'subopt_01': 'Vinhos de Mesa',
        'subopt_02': 'Espumantes',
        'subopt_03': 'Uvas Frescas',
        'subopt_04': 'Uvas Passas',
        'subopt_05': 'Suco de Uva'
    }
    
    subopcao = ['subopt_01', 'subopt_02','subopt_03','subopt_04','subopt_05' ] 
    all_data = {}
    for sub in subopcao:
        sub_data = {}
        for i in range(1970, 2024, 1):
            url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={i}&opcao=opt_05&subopcao={sub}"
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            
            table = soup.find("table", class_="tb_base tb_dados")

            tbody = table.find('tbody')

            rows = tbody.find_all('tr')

            year_data = []
            for row in rows:
                row_data = row.find_all('td')

                if len(row_data) > 1:
                    first_column_data = row_data[0].text.strip()
                    second_column_data = row_data[1].text.strip()
                    third_column_data = row_data[2].text.strip()
                    if search and search.lower() not in first_column_data.lower():
                        continue
                    year_data.append({
                        "País": first_column_data, 
                        "Quantidade Kg": second_column_data, 
                        "Valor US$": third_column_data
                        })
                       
            sub_data[i] = year_data[skip:skip + limit]

        all_data[subopcao_mapping[sub]] = sub_data
           
    return all_data


@router.get("/exportacao",summary="Dados de exportação", description="Carrega dados de exportação de derivados de uva.")
def load_export(limit: int = 10, skip: int = 0, search: str = "", current_user: dict = Depends(oauth2.get_current_active_user) ):
    subopcao_mapping = {
        'subopt_01': 'Vinhos de Mesa',
        'subopt_02': 'Espumantes',
        'subopt_03': 'Uvas Frescas',
        'subopt_04': 'Suco de Uva',
    }

    subopcao = ['subopt_01', 'subopt_02','subopt_03','subopt_04'] 
    all_data = {}
    for sub in subopcao:
        sub_data = {}
        for i in range(1970, 2024, 1):
            url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={i}&opcao=opt_06&subopcao={sub}"
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            
            table = soup.find("table", class_="tb_base tb_dados")

            tbody = table.find('tbody')

            rows = tbody.find_all('tr')

            year_data = []
            for row in rows:
                row_data = row.find_all('td')
                if len(row_data) > 1:
                    first_column_data = row_data[0].text.strip()
                    second_column_data = row_data[1].text.strip()
                    third_column_data = row_data[2].text.strip()
                    if search and search.lower() not in first_column_data.lower():
                        continue
                    year_data.append({
                        "País": first_column_data, 
                        "Quantidade Kg": second_column_data, 
                        "Valor US$": third_column_data
                        })
           
            sub_data[i] = year_data[skip:skip + limit]

        all_data[subopcao_mapping[sub]] = sub_data
    
    return all_data