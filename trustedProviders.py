import getData
import json

def calculate(trustFactor,startDate,endDate,predictionObjectID,predictionObject,*providers):
#Get realized data
    realizedData=json.loads(getData.getproductiondata(startDate,endDate,predictionObjectID))
#Create empty arrays
    selectedProviders=[None] * len(providers)
    accuracyRates=[None] * len(providers)
    i=0
#take date from providers
    for provider in providers:
        selectedProviders[i]=json.loads(getData.getdata(startDate,endDate,provider,predictionObject))
        accuracyRates[i]=100 / len(providers)
        i=i+1

    for selectedProvider in selectedProviders:
        #check if data lengths are equal
        if len(realizedData["data"]) > len(selectedProvider["data"]):
            print("Data lenghts are not equal between realized product and ", selectedProvider["data"][0]["ShortName"])
            print("Trying to syncronize...")
            #compare with date-hour and if they are not equal this means there are missing prediction.So fill that missed production with worst prediction
            for k in range(0,len(realizedData["data"])):
                realizedDate=realizedData["data"][k]["dateText"]
                realizedTime=realizedData["data"][k]["timeText"]
                providerDate=selectedProvider["data"][k]["Instrument"]              
                providerTime=providerDate[11:16]
                providerDate=providerDate[0:10]
                if realizedDate == providerDate and realizedTime == providerTime:
                    continue
                else:
                    print ("One of the missed index on provider is : ", k)
                    print ("Syncronizing...")
                    reserved=selectedProvider
                    error=0
                    temp=""
                    for provider in selectedProviders:
                        if provider == reserved:
                            continue
                        else:
                            dif=abs(realizedData["data"][k]["total"] - provider["data"][k]["Forecast"]) 
                            if dif > error:
                                error=dif
                                temp=provider
                    instrument=realizedDate+"T"+realizedTime+":00.000Z"
                    forecast=temp["data"][k]["Forecast"]
                    shortname=selectedProvider["data"][0]["ShortName"]
                    name=selectedProvider["data"][0]["Name"]
                    selectedProvider["data"].insert(k, {'Name': name,'ShortName': shortname,'Forecast': forecast,'Instrument': instrument})
        #check if is there any missed value in realized production.If yes,delete that hour from all the providers.
        for t in range(0,len(realizedData["data"])-1):    
            currentTime=realizedData["data"][t]["timeText"][:2]
            nextTime=realizedData["data"][t+1]["timeText"][:2]

            if (int(currentTime)+1) == int(nextTime) or (int(currentTime) == 23 and (int(nextTime)) == 00) :
                continue
            else:
                print ("There is a missed index in realized data.This index will be deleted: ",t+1)
                for selectedProvider in selectedProviders:
                    del selectedProvider["data"][t+1]
    #For every provider calculate the most and least trusting provider.
    #This is ranking providers by accuracy rate for every production between providers
    for index in range(0,len(realizedData["data"])):
        realizedDate=realizedData["data"][index]["dateText"]
        realizedTime=realizedData["data"][index]["timeText"]
        providerDate=selectedProvider["data"][index]["Instrument"]              
        providerTime=providerDate[11:16]
        providerDate=providerDate[0:10]
        if realizedDate == providerDate and realizedTime == providerTime:
            i=0
            totalLapse=0
            deltaProviders=[None] * len(providers)
            for selectedProvider in selectedProviders:
                deltaProviders[i]=abs(realizedData["data"][index]["total"] - selectedProvider["data"][index]["Forecast"])
                totalLapse=totalLapse+deltaProviders[i]   
                i=i+1      
            i=0
            deltaPercentageProviders=[None] * len(providers)
            for selectedProvider in selectedProviders:
                deltaPercentageProviders[i]=(100*deltaProviders[i]) / totalLapse
                i=i+1
            i=0
            averageLapsePercentage= 100 / len(providers)
            for selectedProvider in selectedProviders:
                accuracyRates[i] = accuracyRates[i] + (averageLapsePercentage - deltaPercentageProviders[i] ) / float(trustFactor)
                i=i+1
            i=0
            for selectedProvider in selectedProviders:
                if accuracyRates[i] > 95:
                    deliveredRemain =  abs(accuracyRates[i] - 95)
                    accuracyRates[i] = accuracyRates[i] - deliveredRemain
                    j=0
                    for selectedProvider in selectedProviders:
                        if j == i:
                            j=j+1
                            continue
                        else:
                            accuracyRates[j]= accuracyRates[j] +  deliveredRemain/(len(providers)-1)
                            j=j+1
                if accuracyRates[i] < 5:
                    deliveredRemain =  abs(accuracyRates[i] - 5) 
                    accuracyRates[i] = accuracyRates[i] + deliveredRemain 
                    j=0
                    for selectedProvider in selectedProviders:
                        if j == i:
                            j=j+1
                            continue
                        else:
                            accuracyRates[j]= accuracyRates[j] -  deliveredRemain/(len(providers)-1)
                            j=j+1
                i=i+1        
        else:
            print ("This index is not same with realized: ",index)
            print (providerTime+" "+providerDate)
            print (realizedTime+" "+providerDate)
            break
    return accuracyRates
