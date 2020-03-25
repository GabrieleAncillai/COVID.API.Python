import requests
import datetime
import os
API = "https://pomber.github.io/covid19/timeseries.json"
Cases = []
CasesResponse = requests.get(API)
CasesPercentage = []
AproxCases = 0


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def isDate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return False
    return True


def GetCasesFromCountry(text):
    cs = CasesResponse.json().get(text)
    response = {
        "Message": "Datos obtenidos correctamente!",
        "Status": True
    }
    if text and cs != None:
        for x in range(len(cs)):
            if cs[x].get('confirmed') != 0:
                Cases.append(cs[x])

        #print('FINAL CASES: {}'.format(Cases))
        #print('FINAL LEN: {}'.format(len(Cases)))
    else:
        response.update({
            "Message": "Datos erróneos o inexistentes, verifique que esté escribiendo bien el nombre del país",
            "Status": False
        })
    return response


def GetConfirmedPercentage():
    for x in range(len(Cases)):
        if (x+1 < int(len(Cases)) and not(Cases[x].get("DontCount"))):
            resul = ((int(Cases[x+1].get('confirmed')) * 100) /
                     int(Cases[x].get('confirmed')))-100
            CasesPercentage.append(float(resul))


def GetAveragePercentage():
    suma = 0

    for x in range(len(CasesPercentage)):
        suma = suma + float(CasesPercentage[x])

    AveragePercentege = suma / len(CasesPercentage)
    return AveragePercentege


def CheckCasesByDate():
    currentDate = datetime.date.today()
    lastDate = datetime.datetime.strptime(Cases[-1].get('date'), '%Y-%m-%d')

    if currentDate != lastDate.date():
        daysLess = (currentDate - lastDate.date()).days
        print('\nSe ha detectado falta de data con respecto al día de hoy...')
        for x in range(int(daysLess)):
            NewCases = input(
                f'\nIngrese los casos del día {lastDate.date() + datetime.timedelta(days=x+1)}: ')
            Cases.append({
                "date": str(lastDate.date() + datetime.timedelta(days=x+1)),
                "confirmed": NewCases
            })
    else:
        PrintDayCasesPercentage
        print('Todos los casos están actualizados con respecto a hoy...')



def DeleteCasesOutsideDateRange(limitDate):
    newLimit = limitDate

    if isDate(newLimit):
        for x in range(len(Cases)):
            obj_date = datetime.datetime.strptime(
                Cases[x].get('date'), '%Y-%m-%d')
            limit_date = datetime.datetime.strptime(newLimit, '%Y-%m-%d')
            if obj_date.date() < limit_date.date():
                Cases[x].update({
                    "DontCount": True
                })
    else:
        currentDate = datetime.date.today()
        string = [int(s) for s in newLimit.split() if s.isdigit()]
        string = string.pop(0)
        daysLess = datetime.timedelta(days=string)
        newLimit = datetime.datetime.strptime(
            str(currentDate - daysLess), '%Y-%m-%d')
        for x in range(len(Cases)):
            obj_date = datetime.datetime.strptime(
                Cases[x].get('date'), '%Y-%m-%d')
            if obj_date.date() < newLimit.date():
                Cases[x].update({
                    "DontCount": True
                })


# PRINT METHODS

def PrintDayCasesPercentage():
    for x in range(len(CasesPercentage)):
        print('Day {}: {}'.format(x+1, CasesPercentage[x]))


def PrintCases():
    for x in range(len(Cases)):
        print('Day {}: {}'.format(x+1, Cases[x]))


def PrintSummary():
    lastCaseIndex = len(Cases) - 1
    AvPerc = GetAveragePercentage()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    NextPossibleCases = float(
        Cases[lastCaseIndex].get('confirmed')) * ((AvPerc/100)+1)
    print(f"\nProbables casos de mañana {tomorrow}: {NextPossibleCases:.1f}")
    print(f'Promedio de Contagio por día: +{AvPerc:.1f}%\n\n')


# MENU
def Reset():
    option = input('Desea volver al menú principal? (y/n)')
    if option == "y" or option == "Y":
        MainMenu()


def MainMenu():
    cls()
    searchFor = input(
        '\n* Importante: (El nombre del país debe estar en inglés y la primera letra debe ser Mayus.)\n\nEscriba el nombre del país: ')
    data = GetCasesFromCountry(searchFor)
    if data.get('Status'):
        print('\n{}'.format(data.get('Message')))

        searchForDate = input(
            '\nDesea sacar el cálculo a partir de una fecha específica? (y/n): ')

        if searchForDate == "Y" or searchForDate == "y":
            limitDate = input(
                '\nIngrese la fecha en formato (YYYY-MM-DD) o también hace cuantos días (hace 17 días)): ')
            DeleteCasesOutsideDateRange(limitDate)

        CheckCasesByDate()
        GetConfirmedPercentage()
        PrintDayCasesPercentage()
        PrintSummary()

    else:
        print(data.get('Message'))
        MainMenu()

    Reset()


# MAIN
if __name__ == "__main__":
    MainMenu()
