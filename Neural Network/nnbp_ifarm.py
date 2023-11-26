import sys, math, random
import sklearn
from sklearn.preprocessing import MinMaxScaler
#######FINAL VERSION######
####### LAYER STUFF ####
fileContents = list(line.strip() for line in open(sys.argv[1], 'r'))
numinputs = 7
layercounts = [numinputs, 2, 1, 1] # bias
print('Layer counts: ' + ' '.join(str(num) for num in layercounts))

predictions = list(line.strip() for line in open("prediction_data.txt", 'r'))
predictions = [[float(num_str) for num_str in x.split()] for x in predictions]
print("##### PREDICTIONS #####")
print(predictions)
########################

def Transfer(x):
    if math.isnan(x): exit()
    if x < -700: return 0
    if x > 700: return 1 # try catch
    if 1/(1 + math.exp(-x)) == math.inf:
        return 1e+300
    return 1/(1 + math.exp(-x))

def derivativeTransfer(x):

    return x * (1 - x)

def cost(t, y):
    return (t-y)**2 * .5

def dotproduct(list1, list2):
    return sum([list1[i]*list2[i] for i in range(len(list1))])

def layer1BP(t, y, x): #OK
    '''print('layer 1:')
    print('error: ' + str((t - y)), 'x: ' + str(x))
    print('partial: ' + str((t - y) * x))
    print(' ')'''
    return (t - y) * x

def layer2BP(t, y1, y2, x, w):
    '''print('layer 2:')
    print('error: ' + str((t - y1) * derivativeTransfer(y2) * w), 'x: ' + str(x))
    print('partial: ' + str((t - y1) * x * w * derivativeTransfer(y2)))
    print(' ')'''
    return (t - y1) * x * w * derivativeTransfer(y2)

def layer3BP(t, y1, y2, y3, w1, w2list, x):
    '''print('layer 3:')
    print('error: ' + str((t - y1) * w1 * w2list * derivativeTransfer(y2) * derivativeTransfer(y3)), 'x: ' + str(x))
    print('partial: ' + str((t - y1) * w1 * w2list * x * derivativeTransfer(y2) * derivativeTransfer(y3)))
    print(' ')'''
    return (t - y1) * w1 * w2list * x * derivativeTransfer(y2) * derivativeTransfer(y3)

def makeNN(inputoutput, weights):
    layers = [inputoutput[0]]
    currentlayer = layers[0]
    for w in weights:
        newlayer = []
        if w == weights[len(weights) - 1]:
            newlayer = [w[i]*currentlayer[i] for i in range(len(w))]
        else:
            for n in range(0, len(w), len(currentlayer)):
                newlayer.append(Transfer(dotproduct(w[n:n + len(currentlayer)], currentlayer)))
        currentlayer = newlayer
        layers.append(newlayer)
    return layers

def putInWeightAdjustmentList(layers, weights, t, inputs, weightsAdjustinglist):
    #print("inputs", inputs)
    weightsAdjustinglist[weightcount - 1].append(layer1BP(t, layers[3][0], layers[2][0])) #OK
    weightsAdjustinglist[weightcount - 3].append(layer2BP(t, layers[3][0], layers[2][0], layers[1][0], weights[2][0]))
    weightsAdjustinglist[weightcount - 2].append(layer2BP(t, layers[3][0], layers[2][0], layers[1][1], weights[2][0]))
    for otherk in range(2):
        for k in range(numinputs):
            weightsAdjustinglist[numinputs * otherk + k].append(layer3BP(t, layers[3][0], layers[2][0], layers[1][otherk], weights[2][0], weights[1][otherk], inputs[k]))
    return weightsAdjustinglist

def makeRandomWeights():
    return [[random.random() * 2 - 1 for _ in range(layercounts[n] * layercounts[n + 1])] for n in
                       range(len(layercounts) - 1)]

def adjustWeights(weights, weightsAdjustinglist, alpha):
    tempw = weights[0] + weights[1] + weights[2]
    for k in range(len(weightsAdjustinglist)):
        tempw[k] = (tempw[k] + sum(weightsAdjustinglist[k]) * alpha)
    return [tempw[:2 * numinputs], tempw[2 * numinputs: 2 * numinputs + 2], [tempw[-1]]]



def processAllExamples(inputsAndOutputs, weights, weightsAdjustinglist):
    costlist = []
    for inputAndOutput in inputsAndOutputs:
        networkResults = makeNN(inputAndOutput, weights)
        '''print('NETWORK')
        print(networkResults)
        print(' ')'''
        putInWeightAdjustmentList(networkResults, weights, inputAndOutput[1], inputAndOutput[0], weightsAdjustinglist)
        weights = adjustWeights(weights, weightsAdjustinglist, .1)

        #print("MY WEIGHTS:")
        #printWeights(weights)
        weightsAdjustinglist = [[] for _ in range(weightcount)]
        costlist.append(cost(networkResults[3][0], inputAndOutput[1]))
    return weights, sum(costlist)/len(costlist)

def printWeights(weights):
    print(str(weights[0]) + '\n' + str(weights[1]) + '\n' + str(weights[2]))



oldcost = 0
epochsSinceImprovement = 0
inputsOutputsSet = [([float(inp.replace(' ', '')) for inp in fileContents[x].split('=>')[0].split(' ') if inp != ''] + [1], float(fileContents[x].split('=>')[1].replace(' ', ''))) for x in range(len(fileContents))]

scaled_data = []
for input, output in inputsOutputsSet:
    scaled_data.append(input)
scaler = MinMaxScaler()
scaler.fit(scaled_data)
scaled_data = scaler.transform(scaled_data)

for sd in range(len(scaled_data)):
    inputsOutputsSet[sd] = (scaled_data[sd], inputsOutputsSet[sd][1])

print(inputsOutputsSet)

random.shuffle(inputsOutputsSet)
test_data = inputsOutputsSet[:12]
inputsOutputsSet = inputsOutputsSet[12:]
weightslist = makeRandomWeights()
printWeights((weightslist))
weightcount = numinputs*2 + 3

for epoch in range(1000000):
    #print(' ')
    weightslist, currentcost = processAllExamples(inputsOutputsSet, weightslist, [[] for _ in range(weightcount)])
    epochsSinceImprovement += 1
    #print(' ')
    if not epoch:
        oldcost = currentcost
        continue
    if currentcost < oldcost*.95: # if better than 5-10 percentage
        oldcost = currentcost
        epochsSinceImprovement = 0
        print(currentcost)
        printWeights(weightslist)
        if currentcost <= .015:
            print("test data cost: " + str(processAllExamples(test_data, weightslist, [[] for _ in range(weightcount)])[1]))
            print("predictions: ")
            scaled_data = []
            for input in predictions:
                scaled_data.append(input)
            scaler = MinMaxScaler()
            scaler.fit(scaled_data)
            scaled_data = scaler.transform(scaled_data)
            for sd in scaled_data: 
                print(makeNN((sd, -1), weightslist)[-1])
            exit()
    if epochsSinceImprovement > 10000:
        print('started over')
        weightslist = makeRandomWeights()
        epochsSinceImprovement = 0
        oldcost = oldcost * 1.2 #gotta give it a chance to catch up

