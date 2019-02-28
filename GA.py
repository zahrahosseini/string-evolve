print('\n\n\nInitializing-------------------------------')

import string

from timeit import default_timer
from random import choice
import random
import  copy
from random import randint
import csv
import math

# from bisect import bisect
# from itertools import accumulate

# startTime = default_timer()
print('\n\n\n')

targetString = 'IowaState_Cyclone'
genomeLength = 17
initialPopulationSize = 32
populationSize= initialPopulationSize/2#16
newChildSize=initialPopulationSize/4 #8
tournamentSize = 5
mutationRate = 0.03
stopAfterThisManyGenerations = 10000
generationsToWatch = 3
numberOfMutation=int(round(mutationRate*genomeLength*populationSize))#8 #15*16*0.03



def generateGenome(genomeLength):

    return ''.join([choice(list(string.printable + string.digits)) for _ in range(genomeLength)])


def generateInitialPopulation(populationSize):

    return [generateGenome(genomeLength) for _ in range(populationSize)]


def individualFitnessTest(genome):

    fitnessScore = 0

    for i in range(genomeLength):
        if (genome[i] != targetString[i]):
            fitnessScore += 1

    return float(fitnessScore)


def individualFitnessTestWithORD(genome):
    fitnessScore=0
    for i in range(genomeLength):
        fitnessScore+=(ord(genome[i])-ord(targetString[i]))**2
    return float(fitnessScore)

def populationFitnessTest(population,fitnessOption):
    if fitnessOption==0:
        return (map(individualFitnessTestWithORD, population))
    else:
        return (map(individualFitnessTest, population))


def generateFitnessFractions(populationFitnessScores):

    totalPopulationFitness = sum(populationFitnessScores)

    return map(lambda fitnessScore: fitnessScore / totalPopulationFitness, populationFitnessScores)


def generateReproductionTable(fitnessFractions):

    reproductionTable = []
    total = 0

    for f in fitnessFractions:
        total = total + f
        reproductionTable.append(total)

    return reproductionTable


'''
def selectParent(population, reproductionTable):

    return population[bisect(reproductionTable, random())]
'''


# def elitism(population, populationFitnessScores):
	

def selectParent(population, populationFitnessScores,initialPopulationSize):

    tournament = []
    tournamentFitnessScores = []
    randgenerated=random.sample(range(0, initialPopulationSize-1), tournamentSize)
    for i in range(0, tournamentSize):
        selectedIndividualIndex=randgenerated[i]
        tournament.append(''.join(population[selectedIndividualIndex]))
        tournamentFitnessScores.append(populationFitnessScores[selectedIndividualIndex])

    tournamentWinner = tournamentFitnessScores.index(min(tournamentFitnessScores))
    return tournament[tournamentWinner]


# selectedIndividualIndex = randint(0, initialPopulationSize - 1)


def selectTwoParents(population, populationFitnessScores,k):

    tournament = []
    tournamentFitnessScores = []

    for i in range(0, tournamentSize):

        selectedIndividualIndex = randint(0, initialPopulationSize - 1)

        tournament.append(''.join(population[selectedIndividualIndex]))
        tournamentFitnessScores.append(populationFitnessScores[selectedIndividualIndex])

    tournamentWinner = tournamentFitnessScores.index(min(tournamentFitnessScores))
    return tournament[tournamentWinner]





'''
def selectSecondParent(population, populationFitnessScores, firstParent):

    neighborhood = []

    for i in range(firstParent - 5, firstParent):
        neighborhood.append(population[i % initialPopulationSize])

    for i in range(firstParent + 1, firstParent + 6):
        neighborhood.append(population[i % initialPopulationSize])

    return max(neighborhood)
'''


def generateChild(population, populationFitnessScores,initialPopulationSize,uniformCrossOver):

    firstParent = list(selectParent(population, populationFitnessScores,initialPopulationSize))
    secondParent = list(selectParent(population, populationFitnessScores,initialPopulationSize))

    while firstParent == secondParent:
        secondParent = list(selectParent(population, populationFitnessScores,initialPopulationSize))

    child = copy.copy(secondParent)
    if (uniformCrossOver == 1):
        for j in range(genomeLength):
            if (random.random() < 0.5):
                # print("HERE")
                child[j] = firstParent[j]
            else:
                # print("NOTHERE")
                child[j] = secondParent[j]
    else:

    # for i in range(int(genomeLength / 2)):
        geneToSwitch = randint(0, genomeLength - 1)
        child[geneToSwitch] = firstParent[geneToSwitch]
    # print("______________")
    # print(''.join(firstParent)," ",''.join(secondParent)," ",''.join(child))
    # print("______________")
    return ''.join(child)

def generateNewChild12(i,j,population):

    firstParent = list(population[i])
    secondParent = list(population[j])
    # print("&&&", i, ''.join(firstParent))
    # print("&&&", i, ''.join(secondParent))
    child1 = copy.copy(firstParent)
    child2 = copy.copy(secondParent)
    for j in range(genomeLength):
        if (random.random() < 0.5):
            # print("HERE")
            child1[j] = firstParent[j]
            child2[j] = secondParent[j]
        else:
            # print("NOTHERE")
            child1[j] = secondParent[j]
            child2[j] = firstParent[j]
    # print("&&&f", i, ''.join(firstParent))
    # print("&&&s", i, ''.join(secondParent))
    # print("&&&c", i, ''.join(child1))
    # print("&&&c", i, ''.join(child2))
    return  child1,child2


def generateNewChild1(i,j,population,geneToSwitch,uniformCrossOver):

    firstParent = list(population[i])
    secondParent = list(population[j])

    child1 =copy.copy(secondParent)
    # for i in range(int(genomeLength / 2)):
    # geneToSwitch = randint(6, 12)
    child1[geneToSwitch:] = firstParent[geneToSwitch:]

    return child1

def generateNewChild2(i,j,population,geneToSwitch,uniformCrossOver):

    firstParent = list(population[i])
    secondParent = list(population[j])


    child2 =copy.copy(firstParent)
    # for i in range(int(genomeLength / 2)):
    # geneToSwitch = randint(6, 12)
    child2[geneToSwitch:] = secondParent[geneToSwitch:]

    return child2


def generateNewPopulationTournomentSelection(population, populationFitnessScores,initialPopulationSize,uniformCrossOver):
    bestPopulation = population[:newChildSize]
    for i in range(newChildSize):
        child=generateChild(population, populationFitnessScores,len(population),uniformCrossOver)
        bestPopulation.append(child)
    # print("XXXXXXX", len(bestPopulation))
    return bestPopulation

def generateNewPopulation(population, populationFitnessScores,uniformCrossOver):

    # fitnessFractions = generateFitnessFractions(populationFitnessScores)
    # reproductionTable = generateReproductionTable(fitnessFractions)
    # parentno = {}
    parentno=set()
    bestPopulation=population[:newChildSize]
    # print("XXXXXXX",len(bestPopulation), newChildSize)
    for i in range(newChildSize):
        if i not in parentno:
            parentno.add(i)
            parentno.add(i+2)
            geneToSwitch = randint(6, 12)

            if(uniformCrossOver==1):
                child1,child2=generateNewChild12(i,i+2,population)
            else:
                child1=generateNewChild1(i,i+2,population,geneToSwitch,uniformCrossOver)
                child2=generateNewChild2(i,i+2,population,geneToSwitch,uniformCrossOver)
            # print ("&&&",i,''.join(child1))
            # print ("&&&",i+2,''.join(child2))
            bestPopulation.append(''.join(child1))
            bestPopulation.append(''.join(child2))
            # bestPopulation.append(child2)
            # print("XXXXXXX", len(bestPopulation))
    # print("XXXXXXX",len(bestPopulation))
    return bestPopulation
    # return [generateChild(population[:newChildSize], populationFitnessScores) for _ in range(newChildSize)]


def mutate(population, numberOfMutation):
    print("^^^^",numberOfMutation)
    for _ in range(numberOfMutation):
        i=randint(0, genomeLength - 1)
        j=randint(0, populationSize - 1)
        newAlle=choice(string.printable + string.digits)
        #print(i,j,''.join(newAlle), population[j][i])
        output = population[j][:i]
        output += newAlle
        output += population[j][i + 1:]
        # print ("^^^^",population[j],"^^^^",output)
        population[j]=str(output)
        # print ("%%%%",j,population[j],"%%%%",output)

    # for i in range(initialPopulationSize):
    #
    #     if random() < (mutationRate * 1):
    #
    #         mutatedMember = list(population[i])
    #         mutatedMember[randint(0, genomeLength - 1)] = choice(list(string.printable + string.digits))
    #         population[i] = ''.join(mutatedMember)

    return population


def evolve(population,fitnessOption, tournomentSelection,mutationenabled,mutationRate,mrate,numberOfMutation,
           initialPopulationSize, populationSize, newChildSize,uniformCrossOver):

    numberOfGenerations = 1

    populationFitnessScores = populationFitnessTest(population,fitnessOption)
    indexOfMostFitMember = populationFitnessScores.index(min(populationFitnessScores))
    # if fitnessOption == 0:
    #     indexOfMostFitMember = populationFitnessScores.index(min((populationFitnessScores)))
    # else:
    #     indexOfMostFitMember = populationFitnessScores.index(min((populationFitnessScores)))

    mostFitMember = population[indexOfMostFitMember]
    if fitnessOption==0:
        if individualFitnessTestWithORD(targetString)!=0:
            similarityToTargetString = float(populationFitnessScores[indexOfMostFitMember] / individualFitnessTestWithORD(targetString))
        else:
            similarityToTargetString=0
    else:
        similarityToTargetString = (populationFitnessScores[indexOfMostFitMember] / genomeLength)

    print('Generations elapsed:           ' + str(numberOfGenerations) + '===========================================================')
    print('Current most fit member:       ' + ''.join(mostFitMember))
    print('Percent similarity to target:  ' + str(round(similarityToTargetString, 4) * 100) + '%')
    print('\n\n\n')

    while numberOfGenerations < stopAfterThisManyGenerations:

        # print (initialPopulationSize)
        if fitnessOption==0:
            population.sort(key=individualFitnessTestWithORD, reverse=False)
        else:
            population.sort(key=individualFitnessTest, reverse=False)
        for j in range(populationSize):
            if fitnessOption==0:
                print(population[j], individualFitnessTestWithORD(population[j]))
            else:
                print (population[j], individualFitnessTest(population[j]))
        print ("_____First part_________")
        top8=population[:8]
        for j in range(8):
            if fitnessOption==0:
                print(top8[j], individualFitnessTestWithORD(top8[j]))
            else:
                print (top8[j], individualFitnessTest(top8[j]))
        populationFitnessScores = populationFitnessTest(population,fitnessOption)
        # if fitnessOption==0:
        indexOfMostFitMember = populationFitnessScores.index(min((populationFitnessScores)))
        # else:
        #     indexOfMostFitMember = populationFitnessScores.index(min((populationFitnessScores)))
        mostFitMember = population[indexOfMostFitMember]

        similarityToTargetString = (populationFitnessScores[indexOfMostFitMember] / genomeLength)

        if mostFitMember == targetString:
            print('The number of generations elapsed was ' + str(numberOfGenerations))
            populationOutputFile.write('\n\n\n'.join(population))
            populationOutputFile.close()
            return ((mostFitMember)),population,numberOfGenerations
        print ("______After newPop________")
        if tournomentSelection==0:
            population = generateNewPopulation(population, populationFitnessScores,uniformCrossOver)
        else:
            population = generateNewPopulationTournomentSelection(population,populationFitnessScores,populationSize,uniformCrossOver)
        if fitnessOption == 0:
            population.sort(key=individualFitnessTestWithORD, reverse=False)
        else:
            population.sort(key=individualFitnessTest, reverse=False)
        for j in range(populationSize):
            if fitnessOption == 0:
                print (population[j], individualFitnessTestWithORD(population[j]))
            else:
                print (population[j], individualFitnessTest(population[j]))
        print("-----------Mutate----------")
        if mutationenabled==0:
            population=mutate(population, numberOfMutation)
        else:
            mutationRate*=mrate
            numberOfMutation = int(round(mutationRate * genomeLength * populationSize))
            population = mutate(population, numberOfMutation)
        # print (len(population))
        if fitnessOption == 0:
            population.sort(key=individualFitnessTestWithORD, reverse=False)
        else:
            population.sort(key=individualFitnessTest, reverse=False)
        for jj in range(populationSize):
            if fitnessOption == 0:
                print ("****",population[jj], individualFitnessTestWithORD(population[jj]))
            else:
                print ("****",population[jj], individualFitnessTest(population[jj]))
        numberOfGenerations = numberOfGenerations + 1


        if numberOfGenerations % generationsToWatch == 0:


            print('Generations elapsed:           ' + str(numberOfGenerations) + '===========================================================')
            print('Current most fit member:       ' + ''.join(mostFitMember))
            print('Percent similarity to target:  ' + str(round(similarityToTargetString, 4) * 100) + '%')
            print('\n\n\n')

        if mostFitMember == targetString:
            print('The number of generations elapsed was ' + str(numberOfGenerations))
            populationOutputFile.write('\n\n\n'.join(population))
            populationOutputFile.close()
            return ((mostFitMember)),population,numberOfGenerations

    print('The number of generations elapsed was ' + str(numberOfGenerations + 1))
    populationOutputFile.write('\n\n\n'.join(population))
    populationOutputFile.close()
    return ((mostFitMember)),population,numberOfGenerations

ttime=[]
generation=[]
AllScores=[]
bestScores=[]
iterationCount=50

fitnessFunction=0
tournomentSelection=0
mutationenabled=0
uniformCrossOver=0
initialPopulationSize = 32
mrate=0.99
fitnessFunctionOption=[0,1]
tournomentSelectionOption=[0,1]
mutationenabledOption=[0,1]
uniformCrossOverOption=[0,1]
initialPopulationSizeOption=[16,32,64,128,256,512,1024]
mrateOptions=[0.9999,0.999,0.99,1,1.00001,1.0001,1.001]
mutationRate = 0.07
mutationRateOptions=[0.03,0.04,0.05,0.06,0.07]

for fitnessFunctionindex in range(len(fitnessFunctionOption)):
    for tournomentSelectionindex in range(len(tournomentSelectionOption)):
        for uniformCrossOverindex in range(len(uniformCrossOverOption)):
            for initialPopulationSizeindex in range(len(initialPopulationSizeOption)):
                for mutationRateindex in range(len(mutationRateOptions)):
                    for mutationenabledindex in range(len(mutationenabledOption)):
                        mutationRate=mutationRateOptions[mutationRateindex]
                        initialPopulationSize=initialPopulationSizeOption[initialPopulationSizeindex]
                        uniformCrossOver=uniformCrossOverOption[uniformCrossOverindex]
                        mutationenabled=mutationenabledOption[mutationenabledindex]
                        tournomentSelection=tournomentSelectionOption[tournomentSelectionindex]
                        fitnessFunction=fitnessFunctionOption[fitnessFunctionindex]
                        if mutationenabled==1:
                            for mrateindex in range(len(mrateOptions)):
                                ttime = []
                                generation = []
                                AllScores = []
                                bestScores = []
                                mrate=mrateOptions[mrateindex]
                                for k in range(iterationCount):
                                    random.seed(k*7+11)
                                    startTime = default_timer()
                                    scores = []

                                    populationOutputFile = open("finalPopulation.txt", "w")
                                    InitialPopulationOutputFile = open("initialPopulation.txt", "w")
                                    populationSize = initialPopulationSize / 2  # 16
                                    newChildSize = initialPopulationSize / 4
                                    initialPopulation = generateInitialPopulation(initialPopulationSize)
                                    InitialPopulationOutputFile.write('\n\n\n'.join(initialPopulation))
                                    InitialPopulationOutputFile.close()

                                    mostFittest, generatedPopulation, generationNumber = evolve(initialPopulation,
                                                                                                fitnessFunction,
                                                                                                tournomentSelection,
                                                                                                mutationenabled,
                                                                                                mutationRate, mrate,
                                                                                                numberOfMutation,
                                                                                                initialPopulationSize,
                                                                                                populationSize,
                                                                                                newChildSize,
                                                                                                uniformCrossOver)
                                    timeTaken = str(round(default_timer() - startTime, 3))
                                    ttime.append(timeTaken)
                                    generation.append(generationNumber)
                                    if fitnessFunction == 0:
                                        bestScores.append(individualFitnessTest(mostFittest))
                                    else:
                                        bestScores.append(individualFitnessTestWithORD(mostFittest))
                                    if fitnessFunction == 0:
                                        for iindex in range(len(generatedPopulation)):
                                            scores.append(individualFitnessTest(generatedPopulation[iindex]))
                                    else:
                                        for iindex in range(len(generatedPopulation)):
                                            scores.append(individualFitnessTestWithORD(generatedPopulation[iindex]))
                                    AllScores.append(scores)
                                timeFilename = "time" + "Fitness" + str(fitnessFunction) + "TournomentSelection" + str(
                                    tournomentSelection) + \
                                               "mutationEnabled" + str(mutationenabled) + "mutationRate" + str(
                                    mutationRate) + "mrate" + str(mrate) + "UniformCrossOver" + str(
                                    uniformCrossOver) + "populationSize" + \
                                               str(populationSize) + ".csv"
                                scoreFilename = "score" + "Fitness" + str(
                                    fitnessFunction) + "TournomentSelection" + str(tournomentSelection) + \
                                                "mutationEnabled" + str(mutationenabled) + "mutationRate" + str(
                                    mutationRate) + "mrate" + str(mrate) + "UniformCrossOver" + str(
                                    uniformCrossOver) + "populationSize" + \
                                                str(populationSize) + ".csv"
                                generationNumberFilename = "generationNumber" + "Fitness" + str(
                                    fitnessFunction) + "TournomentSelection" + str(tournomentSelection) + \
                                                           "mutationEnabled" + str(
                                    mutationenabled) + "mutationRate" + str(mutationRate) + "mrate" + str(
                                    mrate) + "UniformCrossOver" + str(uniformCrossOver) + "populationSize" + \
                                                           str(populationSize) + ".csv"
                                bestScoresFilename = "bestScores" + "Fitness" + str(
                                    fitnessFunction) + "TournomentSelection" + str(tournomentSelection) + \
                                                     "mutationEnabled" + str(mutationenabled) + "mutationRate" + str(
                                    mutationRate) + "mrate" + str(mrate) + "UniformCrossOver" + str(
                                    uniformCrossOver) + "populationSize" + \
                                                     str(populationSize) + ".csv"
                                with open(timeFilename, 'w') as csvTimefile:
                                    csvwriter = csv.writer(csvTimefile)
                                    csvwriter.writerow(ttime)
                                with open(scoreFilename, 'w') as csvScoreAvgfile:
                                    csvwriter = csv.writer(csvScoreAvgfile)
                                    for sindex in range(len(AllScores)):
                                        csvwriter.writerow(AllScores[sindex])
                                with open(generationNumberFilename, 'w') as csvGenerationfile:
                                    csvwriter = csv.writer(csvGenerationfile)
                                    csvwriter.writerow(generation)
                                with open(bestScoresFilename, 'w') as csvBestScorefile:
                                    csvwriter = csv.writer(csvBestScorefile)
                                    csvwriter.writerow(bestScores)
                        else:
                            ttime = []
                            generation = []
                            AllScores = []
                            bestScores = []
                            for k in range(iterationCount):
                                random.seed(k * 7 + 11)
                                startTime = default_timer()
                                scores = []

                                populationOutputFile = open("finalPopulation.txt", "w")
                                InitialPopulationOutputFile = open("initialPopulation.txt", "w")
                                populationSize = initialPopulationSize / 2  # 16
                                newChildSize = initialPopulationSize / 4
                                initialPopulation = generateInitialPopulation(initialPopulationSize)
                                InitialPopulationOutputFile.write('\n\n\n'.join(initialPopulation))
                                InitialPopulationOutputFile.close()

                                mostFittest, generatedPopulation, generationNumber = evolve(initialPopulation,
                                                                                            fitnessFunction,
                                                                                            tournomentSelection,
                                                                                            mutationenabled,
                                                                                            mutationRate, mrate,
                                                                                            numberOfMutation,
                                                                                            initialPopulationSize,
                                                                                            populationSize,
                                                                                            newChildSize,
                                                                                            uniformCrossOver)
                                timeTaken = str(round(default_timer() - startTime, 3))
                                ttime.append(timeTaken)
                                generation.append(generationNumber)
                                if fitnessFunction == 0:
                                    bestScores.append(individualFitnessTest(mostFittest))
                                else:
                                    bestScores.append(individualFitnessTestWithORD(mostFittest))
                                if fitnessFunction == 0:
                                    for iindex in range(len(generatedPopulation)):
                                        scores.append(individualFitnessTest(generatedPopulation[iindex]))
                                else:
                                    for iindex in range(len(generatedPopulation)):
                                        scores.append(individualFitnessTestWithORD(generatedPopulation[iindex]))
                                AllScores.append(scores)
                            timeFilename = "time" + "Fitness" + str(fitnessFunction) + "TournomentSelection" + str(
                                tournomentSelection) + \
                                           "mutationEnabled" + str(mutationenabled) + "mutationRate" + str(
                                mutationRate) + "mrate" + str(mrate) + "UniformCrossOver" + str(
                                uniformCrossOver) + "populationSize" + \
                                           str(populationSize) + ".csv"
                            scoreFilename = "score" + "Fitness" + str(fitnessFunction) + "TournomentSelection" + str(
                                tournomentSelection) + \
                                            "mutationEnabled" + str(mutationenabled) + "mutationRate" + str(
                                mutationRate) + "mrate" + str(mrate) + "UniformCrossOver" + str(
                                uniformCrossOver) + "populationSize" + \
                                            str(populationSize) + ".csv"
                            generationNumberFilename = "generationNumber" + "Fitness" + str(
                                fitnessFunction) + "TournomentSelection" + str(tournomentSelection) + \
                                                       "mutationEnabled" + str(mutationenabled) + "mutationRate" + str(
                                mutationRate) + "mrate" + str(mrate) + "UniformCrossOver" + str(
                                uniformCrossOver) + "populationSize" + \
                                                       str(populationSize) + ".csv"
                            bestScoresFilename = "bestScores" + "Fitness" + str(
                                fitnessFunction) + "TournomentSelection" + str(tournomentSelection) + \
                                                 "mutationEnabled" + str(mutationenabled) + "mutationRate" + str(
                                mutationRate) + "mrate" + str(mrate) + "UniformCrossOver" + str(
                                uniformCrossOver) + "populationSize" + \
                                                 str(populationSize) + ".csv"
                            with open(timeFilename, 'w') as csvTimefile:
                                csvwriter = csv.writer(csvTimefile)
                                csvwriter.writerow(ttime)
                            with open(scoreFilename, 'w') as csvScoreAvgfile:
                                csvwriter = csv.writer(csvScoreAvgfile)
                                for sindex in range(len(AllScores)):
                                    csvwriter.writerow(AllScores[sindex])
                            with open(generationNumberFilename, 'w') as csvGenerationfile:
                                csvwriter = csv.writer(csvGenerationfile)
                                csvwriter.writerow(generation)
                            with open(bestScoresFilename, 'w') as csvBestScorefile:
                                csvwriter = csv.writer(csvBestScorefile)
                                csvwriter.writerow(bestScores)





# for k in range(iterationCount):
#     startTime = default_timer()
#     scores = []
#
#     populationOutputFile = open("finalPopulation.txt", "w")
#     InitialPopulationOutputFile = open("initialPopulation.txt", "w")
#     populationSize= initialPopulationSize/2#16
#     newChildSize=initialPopulationSize/4
#     initialPopulation = generateInitialPopulation(initialPopulationSize)
#     InitialPopulationOutputFile.write('\n\n\n'.join(initialPopulation))
#     InitialPopulationOutputFile.close()
#
#     mostFittest,generatedPopulation,generationNumber= evolve(initialPopulation,fitnessFunction,tournomentSelection,
#                mutationenabled,mutationRate,mrate,numberOfMutation,
#                initialPopulationSize,populationSize,newChildSize,
#                uniformCrossOver)
#     timeTaken = str(round(default_timer() - startTime, 3))
#     ttime.append(timeTaken)
#     generation.append(generationNumber)
#     if fitnessFunction==0:
#         bestScores.append(individualFitnessTest(mostFittest))
#     else:
#         bestScores.append(individualFitnessTestWithORD(mostFittest))
#     if fitnessFunction == 0:
#         for iindex in range(len(generatedPopulation)):
#             scores.append(individualFitnessTest(generatedPopulation[iindex]))
#     else:
#         for iindex in range(len(generatedPopulation)):
#             scores.append(individualFitnessTestWithORD(generatedPopulation[iindex]))
#     AllScores.append(scores)
# timeFilename = "time"+"Fitness"+str(fitnessFunction)+"TournomentSelection"+str(tournomentSelection)+\
#            "mutationEnabled"+str(mutationenabled)+"mutationRate"+str(mutationRate)+"mrate"+str(mrate)+"UniformCrossOver"+str(uniformCrossOver)+"populationSize"+\
#            str(populationSize)+".csv"
# scoreFilename = "score" + "Fitness" + str(fitnessFunction) + "TournomentSelection" + str(tournomentSelection) +\
#            "mutationEnabled" + str(mutationenabled)+"mutationRate"+str(mutationRate)+"mrate"+str(mrate)+"UniformCrossOver" + str(uniformCrossOver) +"populationSize" + \
#                 str(populationSize) +".csv"
# generationNumberFilename = "generationNumber"+"Fitness"+str(fitnessFunction)+"TournomentSelection"+str(tournomentSelection)+\
#            "mutationEnabled"+str(mutationenabled)+"mutationRate"+str(mutationRate)+"mrate"+str(mrate)+"UniformCrossOver"+str(uniformCrossOver)+"populationSize"+\
#            str(populationSize)+".csv"
# bestScoresFilename = "bestScores"+"Fitness"+str(fitnessFunction)+"TournomentSelection"+str(tournomentSelection)+\
#            "mutationEnabled"+str(mutationenabled)+"mutationRate"+str(mutationRate)+"mrate"+str(mrate)+"UniformCrossOver"+str(uniformCrossOver)+"populationSize"+\
#            str(populationSize)+".csv"
# with open(timeFilename, 'w') as csvTimefile:
#     csvwriter = csv.writer(csvTimefile)
#     csvwriter.writerow(ttime)
# with open(scoreFilename, 'w') as csvScoreAvgfile:
#     csvwriter = csv.writer(csvScoreAvgfile)
#     for sindex in range(len(AllScores)):
#         csvwriter.writerow(AllScores[sindex])
# with open(generationNumberFilename, 'w') as csvGenerationfile:
#     csvwriter = csv.writer(csvGenerationfile)
#     csvwriter.writerow(generation)
# with open(bestScoresFilename, 'w') as csvBestScorefile:
#     csvwriter = csv.writer(csvBestScorefile)
#     csvwriter.writerow(bestScores)






'''
# ============================ Testing Stuff is Below / may contain old nonfunctional code ====================================== #
initialPopulation = generateInitialPopulation(5)
populationFitnessScores = populationFitnessTest(initialPopulation)
fitnessFractions = generateFitnessFractions(populationFitnessScores)
reproductionTable = generateReproductionTable(fitnessFractions)

print(initialPopulation)
print(reproductionTable)
print('\n\n\n\n')

print(selectFirstParent(reproductionTable))
'''



