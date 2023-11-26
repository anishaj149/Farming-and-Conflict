import csv

Asia9195 = []
Asia9600 = []
Asia0105 = []
Asia0610 = []

ME9195 =[]
ME9600 =[]
ME0105 =[]
ME0610 =[]

NA9195 =[]
NA9600 =[]
NA0105 =[]
NA0610 =[]

LA9195 =[]
LA9600 =[]
LA0105 =[]
LA0610 =[]


Afric9195 =[]
Afric9600 =[]
Afric0105 =[]
Afric0610 =[]

Euro9195 =[]
Euro9600 =[]
Euro0105 =[]
Euro0610 =[]

with open('alldata.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        classification = 0
        if row[0] == "positive": classification = 4
        elif row[0] == "slightly_pos": classification = 1
        elif row[0] == "negative": classification = -4
        elif row[0] == "slightly_neg": classification = -1

        if row[1].find('Asia') != -1: 
            if row[1].find('91') != -1:
                Asia9195.append(classification)
            elif row[1].find('96') != -1:
                Asia9600.append(classification)
            elif row[1].find('01') != -1:
                Asia0105.append(classification)
            elif row[1].find('06') != -1:
                Asia0610.append(classification)
        elif row[1].find('Afric') != -1: 
            if row[1].find('91') != -1:
                Afric9195.append(classification)
            elif row[1].find('96') != -1:
                Afric9600.append(classification)
            elif row[1].find('01') != -1:
                Afric0105.append(classification)
            elif row[1].find('06') != -1:
                Afric0610.append(classification)
        elif row[1].find('ME') != -1: 
            if row[1].find('91') != -1:
                ME9195.append(classification)
            elif row[1].find('96') != -1:
                ME9600.append(classification)
            elif row[1].find('01') != -1:
                ME0105.append(classification)
            elif row[1].find('06') != -1:
                ME0610.append(classification)
        elif row[1].find('NA') != -1: 
            if row[1].find('91') != -1:
                NA9195.append(classification)
            elif row[1].find('96') != -1:
                NA9600.append(classification)
            elif row[1].find('01') != -1:
                NA0105.append(classification)
            elif row[1].find('06') != -1:
                NA0610.append(classification)
        elif row[1].find('LA') != -1: 
            if row[1].find('91') != -1:
                LA9195.append(classification)
            elif row[1].find('96') != -1:
                LA9600.append(classification)
            elif row[1].find('01') != -1:
                LA0105.append(classification)
            elif row[1].find('06') != -1:
                LA0610.append(classification)
        elif row[1].find('Euro') != -1: 
            if row[1].find('91') != -1:
                Euro9195.append(classification)
            elif row[1].find('96') != -1:
                Euro9600.append(classification)
            elif row[1].find('01') != -1:
                Euro0105.append(classification)
            elif row[1].find('06') != -1:
                Euro0610.append(classification)
with open("yearcountrysentiment.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Asia91-95"] + Asia9195)
    writer.writerow(["Asia9600"] + Asia9600) 
    writer.writerow(["Asia0105"] +Asia0105)
    writer.writerow(["Asia0610"] + Asia0610)

    writer.writerow(["ME9195"] + ME9195)
    writer.writerow(["ME9600"] + ME9600) 
    writer.writerow(["ME0105"] + ME0105)
    writer.writerow(["ME0610"] + ME0610)

    writer.writerow(["NA9195"] + NA9195)
    writer.writerow(["NA9600"] + NA9600)
    writer.writerow(["NA0105"] + NA0105)
    writer.writerow(["NA0610"] + NA0610)

    writer.writerow(["LA9195"] + LA9195)
    writer.writerow(["LA9600"] + LA9600)
    writer.writerow(["LA0105"] + LA0105)
    writer.writerow(["LA0610"] + LA0610)

    writer.writerow(["Afric9195"] + Afric9195)
    writer.writerow(["Afric9600"] + Afric9600)
    writer.writerow(["Afric0105"] + Afric0105)
    writer.writerow(["Afric0610"] + Afric0610)

    writer.writerow(["Euro9195"] + Euro9195)
    writer.writerow(["Euro9600"] + Euro9600)
    writer.writerow(["Euro0105"] + Euro0105)
    writer.writerow(["Euro0610"] + Euro0610)
print(sum(Asia9195)/len(Asia9195), sum(Asia9600)/len(Asia9600),sum(Asia0105)/len(Asia0105),sum(Asia0610)/len(Asia0610), sum(ME9195 )/len(ME9195),
    sum(ME9600)/len(ME9600),sum(ME0105)/len(ME0105),sum(ME0610 )/len(ME0610 ),sum(NA9195 )/len(NA9195 ),sum(NA9600 )/len(NA9600 ), sum(NA0105)/len(NA0105),
    sum(NA0610 )/len(NA0610 ),sum(LA9195 )/len(LA9195 ), sum(LA9600 )/len(LA9600 ), sum(LA0105 )/len(LA0105 ),sum(LA0610 )/len(LA0610 ),
    sum(Afric9195)/len(Afric9195),sum(Afric9600)/len(Afric9600),sum(Afric0105)/len(Afric0105),sum(Afric0610)/len(Afric0610),sum(Euro9195)/len(Euro9195),
    sum(Euro9600)/len(Euro9600),sum(Euro0105)/len(Euro0105),sum(Euro0610)/len(Euro0610))
        
        