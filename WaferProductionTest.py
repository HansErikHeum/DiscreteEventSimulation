
import sys
import math


""" @authors: Herman Zahl & Hans Erik Heum"""


class Batch:
    BEFORE_JOINING_BUFFER = 0
    IN_BUFFER = 1
    IN_MACHINE = 2
    FINISHED_IN_INVENTORY = 3

    def __init__(self, numberOfWafers, code):
        self.numberOfWafers = numberOfWafers
        self.code = code
        self.state = Batch.BEFORE_JOINING_BUFFER

    def getNumberOfWafers(self):
        return self.numberOfWafers

    def getCode(self):
        return self.code

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state


class Buffer:
    def __init__(self, name, capacity, machine):
        self.name = name
        self.capacity = capacity
        # List, must be handled as a FIFO
        self.batchesInBuffer = []
        self.machine = machine

    def getName(self):
        return self.name

    def getBatchesInBuffer(self):
        return self.batchesInBuffer

    def getNextBatchInQueue(self):
        if self.isEmpty():
            return None
        return self.batchesInBuffer[0]

    def addBatch(self, batch):
        self.batchesInBuffer.append(batch)

    def getMachine(self):
        return self.machine

    def removeBatch(self, batch):
        self.batchesInBuffer.remove(batch)

    def isEmpty(self):
        return len(self.batchesInBuffer) == 0

    def getNumberOfBatchesInBuffer(self):
        return len(self.batchesInBuffer)

    def hasSpaceForAnotherBatch(self, newBatch):
        currentTotalWafers = 0
        for batch in self.batchesInBuffer:
            currentTotalWafers += batch.getNumberOfWafers()
        if (currentTotalWafers + newBatch.getNumberOfWafers()) > self.capacity:
            return False
        else:
            return True

    def resetBuffer(self):
        self.batchesInBuffer = []


class Task:
    def __init__(self, name, machine, inputBuffer, outputBuffer, loadingTime, processingTime):
        self.name = name
        self.machine = machine
        self.inputBuffer = inputBuffer
        self.outputBuffer = outputBuffer
        # load and unload time, which is the same, and is always 2 secs
        self.loadTime = loadingTime
        self.processingTime = processingTime

    def getName(self):
        return self.name

    def getMachine(self):
        return self.machine

    def getInputBuffer(self):
        return self.inputBuffer

    def getOutputBuffer(self):
        return self.outputBuffer

    def getLoadTime(self):
        return self.loadTime

    def getProcessingTime(self):
        return self.processingTime


class Machine:

    CHRONOLOGICAL_TASK_SELECTION = 1
    REVERSE_CHRONOLOGICAL_TASK_SELECTION = 2
    CHOOSE_BUFFER_WITH_MOST_BATCHES = 3

    def __init__(self, name):
        self.name = name
        self.listOfTasks = []
        self.listOfBuffers = []
        self.workingOnBatch = None

    def getName(self):
        return self.name

    def getListOfBuffers(self):
        return self.listOfBuffers

    def getWorkingOnBatch(self):
        return self.workingOnBatch

    def selectNextBatch(self, logic):
        if logic == Machine.CHRONOLOGICAL_TASK_SELECTION:
            nextBatch, task = self.chronologicalTaskSelection()
        elif logic == Machine.REVERSE_CHRONOLOGICAL_TASK_SELECTION:
            nextBatch, task = self.reverseChronologicalTaskSelection()
        elif logic == Machine.CHOOSE_BUFFER_WITH_MOST_BATCHES:
            nextBatch, task = self.chooseBufferWithMostBatches()
        return nextBatch, task

    def chronologicalTaskSelection(self):
        batch = None
        currentTask = None
        for task in self.listOfTasks:
            batch = self.checkIfTaskCanBeDoneAndReturnBatch(task)
            currentTask = task
            if batch != None:
                break
        return batch, currentTask

    def reverseChronologicalTaskSelection(self):
        reversedTaskList = self.listOfTasks.copy()
        reversedTaskList.reverse()
        batch = None
        currentTask = None
        for task in reversedTaskList:
            batch = self.checkIfTaskCanBeDoneAndReturnBatch(task)
            currentTask = task
            if batch != None:
                break
        return batch, currentTask

    # makes a priority-list based on the buffers with the most batches in its queue

    def chooseBufferWithMostBatches(self):
        batch = None
        currentTask = None
        listOfTasksBuffersWithMostBatches = self.makePriorityListOfBuffers()
        for task in listOfTasksBuffersWithMostBatches:
            batch = self.checkIfTaskCanBeDoneAndReturnBatch(task)
            currentTask = task
            if batch != None:
                break
        return batch, currentTask

    def makePriorityListOfBuffers(self):
        priorityBufferQueue = []
        for task in self.listOfTasks:
            position = 0
            while position < len(priorityBufferQueue):
                otherTask = priorityBufferQueue[position]
                if otherTask.getInputBuffer().getNumberOfBatchesInBuffer() > task.getInputBuffer().getNumberOfBatchesInBuffer():
                    break
                position += 1
            priorityBufferQueue.insert(position, task)
        return priorityBufferQueue

    def checkIfTaskCanBeDoneAndReturnBatch(self, task):
        # If it is no batches in the inputBuffer
        if task.getInputBuffer().isEmpty():
            return None
        tasksNextBatch = task.getInputBuffer().getNextBatchInQueue()
        if tasksNextBatch.getState() != Batch.IN_BUFFER:
            return None
        # has the outputbuffer capacity for another batch?
        if not task.getOutputBuffer().hasSpaceForAnotherBatch(tasksNextBatch):
            return None
        # if the return is not None, it has space for another batch
        return tasksNextBatch

    def addTask(self, task):
        self.listOfTasks.append(task)

    def addBuffer(self, buffer):
        self.listOfBuffers.append(buffer)

    def setWorkingOnBatch(self, batch):
        self.workingOnBatch = batch

    def resetMachine(self):
        self.workingOnBatch = None


class Plant:
    def __init__(self, name):
        self.name = name
        self.buffers = dict()
        self.tasks = dict()
        self.machines = dict()
        self.batches = []

    def getName(self):
        return self.name

    def getTasks(self):
        return self.tasks.values()

    def getMachines(self):
        return self.machines

    def getBatches(self):
        return self.batches

    def newBatch(self, numberOfWafers, code):
        newBatch = Batch(numberOfWafers, code)
        self.batches.append(newBatch)
        return newBatch

    def newBuffer(self, nameOfBuffersTask, capacity, machine):
        newBuffer = Buffer(nameOfBuffersTask, capacity, machine)
        self.buffers[nameOfBuffersTask] = newBuffer
        machine.addBuffer(newBuffer)
        return newBuffer

    def getBuffers(self):
        return self.buffers.values()

    def deleteBuffer(self, nameOfBuffersTask):
        del self.buffers[nameOfBuffersTask]

    def newTask(self, name, machine, inputBuffer, outputBuffer, loadingTime, processingTime):
        newTask = Task(name, machine, inputBuffer, outputBuffer,
                       loadingTime, processingTime)
        machine.addTask(newTask)
        self.tasks[name] = newTask
        return newTask

    def deleteTask(self, name):
        del self.tasks[name]

    def newMachine(self, name):
        newMachine = Machine(name)
        self.machines[name] = newMachine
        return newMachine

    def deleteMachine(self, name):
        del self.machines[name]

    def findFirstTask(self):
        return self.tasks["1"]

    def batchEntersBuffer(self, batch, buffer):
        batch.setState(Batch.IN_BUFFER)
        # if the batch enters the last buffer
        if buffer.getName() == "finished inventory":
            batch.setState(Batch.FINISHED_IN_INVENTORY)
        buffer.addBatch(batch)

    def loadMachineFromBuffer(self, batch, buffer, machine):
        machine.setWorkingOnBatch(batch)
        batch.setState(Batch.IN_MACHINE)
        buffer.removeBatch(batch)

    def batchFinishedOperatingOnMachine(self, machine):
        machine.setWorkingOnBatch(None)

    def resetPlant(self):
        for machine in self.machines:
            self.machines[machine].resetMachine()
        for buffer in self.buffers:
            self.buffers[buffer].resetBuffer()


class Event:
    BATCH_ENTERS_FIRST_BUFFER = 0
    BATCH_ENTERS_BUFFER = 1
    MACHINE_FINISHED_OPERATING_ON_BATCH = 2
    LOAD_MACHINE_FROM_BUFFER = 3
    FINISHED = 4

    def __init__(self, type, number, date):
        self.type = type
        self.number = number
        self.date = date
        self.batch = None
        self.machine = None
        self.task = None

    def getType(self):
        return self.type

    def getNumber(self):
        return self.number

    def getDate(self):
        return self.date

    def setBatch(self, batch):
        self.batch = batch

    def getBatch(self):
        return self.batch

    def setMachine(self, machine):
        self.machine = machine

    def getMachine(self):
        return self.machine

    def setTask(self, task):
        self.task = task

    def getTask(self):
        return self.task


class Schedule:
    def __init__(self, plant):
        self.plant = plant
        self.schedule = []
        self.currentDate = 0
        self.batches = []
        self.eventNumber = 0
        self.testHandCodedEventNumber = 0

    def getSchedule(self):
        return self.schedule

    def isScheduleEmpty(self):
        return len(self.schedule) == 0

    def popFirstEvent(self):
        return self.schedule.pop(0)

    def insertEvent(self, event):
        position = 0
        while position < len(self.schedule):
            otherEvent = self.schedule[position]
            if otherEvent.getDate() > event.getDate():
                break
            position += 1
        self.schedule.insert(position, event)

    def scheduleEvent(self, type, date, batch, task):
        self.eventNumber += 1
        event = Event(type, self.eventNumber, date)
        event.setBatch(batch)
        event.setTask(task)
        self.insertEvent(event)
        return event

    def scheduleEventBatchEntersFirstBuffer(self):
        if len(self.batches) == 0:
            return
        batch = self.batches.pop(0)
        firstTask = self.plant.findFirstTask()
        date = self.currentDate + firstTask.getLoadTime()
        return self.scheduleEvent(Event.BATCH_ENTERS_FIRST_BUFFER, date, batch, firstTask)

    def scheduleEventBatchEntersBuffer(self, batch, task):
        date = self.currentDate + task.getLoadTime()
        return self.scheduleEvent(Event.BATCH_ENTERS_BUFFER, date, batch, task)

    def scheduleEventLoadMachineFromBuffer(self, batch, task):
        task.getMachine().setWorkingOnBatch(batch)
        date = self.currentDate + task.getLoadTime()
        return self.scheduleEvent(Event.LOAD_MACHINE_FROM_BUFFER, date, batch, task)

    def scheduleEventMachineFinishedOperatingOnBatch(self, batch, task):
        date = self.currentDate + \
            (task.getProcessingTime()*batch.getNumberOfWafers())
        return self.scheduleEvent(Event.MACHINE_FINISHED_OPERATING_ON_BATCH, date, batch, task)


class Simulator:
    # logic of batch introduction:
    LOAD_BATCHES_WHEN_MORE_SPACE_IS_AVAILABLE_IN_FIRST_BUFFER = 1

    def __init__(self, plant, schedule):
        self.plant = plant
        self.schedule = schedule
        self.execution = []
        self.machineTaskChoosingLogic = None
        self.introduceNewBatchesLogic = None
        self.batchesMade = None

    def getSchedule(self):
        return self.schedule

    def getExecution(self):
        return self.execution

    def getMachineTaskChoosingLogic(self):
        return self.machineTaskChoosingLogic

    def setMachineTaskChoosingLogic(self, logic):
        self.machineTaskChoosingLogic = logic

    def getIntroduceNewBatchesLogic(self):
        return self.introduceNewBatchesLogic

    def setIntroduceNewBatchesLogic(self, logic):
        self.introduceNewBatchesLogic = logic

    def getBatchesMade(self):
        return self.batchesMade

    def setBatchesMade(self, batchesMade):
        self.batchesMade = batchesMade

    def simulationLoop(self, numberOfWafersTotal, batchSize):
        batchesMade = 0
        batchNumber = 1
        while batchesMade < numberOfWafersTotal:
            newBatch = self.plant.newBatch(batchSize, batchNumber)
            batchNumber += 1
            batchesMade += batchSize
            self.schedule.batches.append(newBatch)
        self.setBatchesMade(batchesMade)
        self.schedule.scheduleEventBatchEntersFirstBuffer()

        while not self.schedule.isScheduleEmpty():
            event = self.schedule.popFirstEvent()
            self.execution.append(event)
            self.executeEvent(event)

    def simulationHardCodeStart(self):
        while not self.schedule.isScheduleEmpty():
            event = self.schedule.popFirstEvent()
            self.execution.append(event)
            self.executeEvent(event)

    def executeEvent(self, event):
        self.schedule.currentDate = event.getDate()
        # ___________________________________________________
        if event.getType() == Event.BATCH_ENTERS_FIRST_BUFFER:
            self.executeEventBatchEntersFirstBuffer(event)

        elif event.getType() == Event.BATCH_ENTERS_BUFFER:
            self.executeEventBatchEntersBuffer(event)

        elif event.getType() == Event.LOAD_MACHINE_FROM_BUFFER:
            self.executeEventLoadMachineFromBuffer(event)

        elif event.getType() == Event.MACHINE_FINISHED_OPERATING_ON_BATCH:
            self.executeEventMachineFinishedOperatingOnBatch(event)

    def executeEventBatchEntersFirstBuffer(self, event):
        batch = event.getBatch()
        toBuffer = event.getTask().getInputBuffer()
        self.plant.batchEntersBuffer(batch, toBuffer)
        self.machinesLookForWork()

    def executeEventBatchEntersBuffer(self, event):
        batch = event.getBatch()
        toBuffer = event.getTask().getOutputBuffer()
        machine = event.task.getMachine()
        self.plant.batchFinishedOperatingOnMachine(machine)
        self.plant.batchEntersBuffer(batch, toBuffer)
        self.machinesLookForWork()

    def executeEventLoadMachineFromBuffer(self, event):
        batch = event.getBatch()
        buffer = event.task.getInputBuffer()
        machine = event.task.getMachine()
        self.plant.loadMachineFromBuffer(batch, buffer, machine)
        self.schedule.scheduleEventMachineFinishedOperatingOnBatch(
            batch, event.task)
        self.machinesLookForWork()

        # Adds another batch into the first buffer, when a batch is taken from it (when space is available)
        if self.getIntroduceNewBatchesLogic() == Simulator.LOAD_BATCHES_WHEN_MORE_SPACE_IS_AVAILABLE_IN_FIRST_BUFFER and buffer.getName() == '1':
            self.schedule.scheduleEventBatchEntersFirstBuffer()

    def executeEventMachineFinishedOperatingOnBatch(self, event):
        batch = event.getBatch()
        machine = event.getMachine()
        task = event.getTask()
        # self.plant.batchFinishedOperatingOnMachine(batch, machine)
        self.schedule.scheduleEventBatchEntersBuffer(batch, task)

    def machinesLookForWork(self):
        for machine in self.plant.machines:
            # if the machine is working on something
            if self.plant.machines[machine].getWorkingOnBatch() != None:
                continue
            # if the machine is the final inventory
            if self.plant.machines[machine].getName() == "4":
                continue
            batchToWorkOn, task = self.plant.machines[machine].selectNextBatch(
                self.machineTaskChoosingLogic)
            if batchToWorkOn != None:
                self.schedule.scheduleEventLoadMachineFromBuffer(
                    batchToWorkOn, task)


class Optimizer:
    def __init__(self, plant, numberOfWafersTotal):
        self.plant = plant
        self.numberOfWafersTotal = numberOfWafersTotal
        self.simulations = {}
        self.machineTaskChoosingLogics = [Machine.CHRONOLOGICAL_TASK_SELECTION,
                                          Machine.REVERSE_CHRONOLOGICAL_TASK_SELECTION, Machine.CHOOSE_BUFFER_WITH_MOST_BATCHES]
        self.introduceNewBatchesLogics = [
            Simulator.LOAD_BATCHES_WHEN_MORE_SPACE_IS_AVAILABLE_IN_FIRST_BUFFER]
        self.batchTypes = [20, 25, 40, 50]
        self.quickestTime = 100000000
        self.bestSimulation = None

    def getSimulations(self):
        return self.simulations

    def getMachineTaskChoosingLogics(self):
        return self.machineTaskChoosingLogics

    def getIntroduceNewBatchesLogic(self):
        return self.introduceNewBatchesLogics

    def getBatchTypes(self):
        return self.batchTypes

    def getQuickestTime(self):
        return self.quickestTime

    def getBestSimulation(self):
        return self.bestSimulation

    def startOptimization(self):
        simulationNumber = 1
        quickestTime = 100000000000000
        bestSimulation = None

        for batchSize in self.batchTypes:
            for machineLogic in self.machineTaskChoosingLogics:
                for batchIntroduceLogic in self.introduceNewBatchesLogics:
                    self.plant.resetPlant()
                    simulationDict = {"machineLogic": machineLogic,
                                      "batchIntroduceLogic": batchIntroduceLogic, "batchSize": batchSize}
                    timeItTook, batchesMade = self.startSimulationAndReturnTimeItTookAndBatchesMade(
                        machineLogic, batchIntroduceLogic, batchSize)
                    simulationDict["batchesMade"] = batchesMade
                    simulationDict["timeToSimulate"] = timeItTook

                    if timeItTook < quickestTime:
                        quickestTime = timeItTook
                        bestSimulation = (
                            "simulation: " + str(simulationNumber))
                    self.simulations["simulation: " +
                                     str(simulationNumber)] = simulationDict
                    simulationNumber += 1
        self.quickestTime = quickestTime
        self.bestSimulation = bestSimulation

    def startSimulationAndReturnTimeItTookAndBatchesMade(self, machineLogic, batchIntroduceLogic, batchSize):
        schedule = Schedule(self.plant)
        simulator = Simulator(self.plant, schedule)
        simulator.setMachineTaskChoosingLogic(machineLogic)
        simulator.setIntroduceNewBatchesLogic(batchIntroduceLogic)
        simulator.simulationLoop(self.numberOfWafersTotal, batchSize)
        # returns the time at the last event happening, aka the time the whole simulation took
        timeItTook = simulator.getExecution()[-1].getDate()
        batchesMade = simulator.getBatchesMade()
        return timeItTook, batchesMade


class Printer:
    def __init__(self, plant):
        self.plant = plant

    def printPlantState(self, outputFile):
        try:
            outputFile = open(outputFile, "w")
        except:
            sys.stderr.write("Unable to open file {0:s}\n".format(outputFile))
            sys.stderr.flush()
            return

        outputFile.write(
            "The current state of {0:s} \n".format(self.plant.getName()))
        machines = self.plant.getMachines()
        for machine in machines:
            self.printMachine(machines[machine], outputFile)
        batches = self.plant.getBatches()
        outputFile.write("State of batches: \n")
        for batch in batches:
            self.printBatchState(batch, outputFile)

    def printMachine(self, machine, outputFile):
        outputFile.write("machine {0:s}\n".format(machine.getName()))
        for buffer in machine.getListOfBuffers():
            outputFile.write(
                "\t Queue of batches in buffer {0:s} :".format(buffer.getName()))
            for batch in buffer.getBatchesInBuffer():
                outputFile.write(" {0:d}".format(batch.getCode()))
            outputFile.write("\n")
        outputFile.write(
            "\t Is currently working on batch:")
        if machine.getWorkingOnBatch() != None:
            outputFile.write(" {0:d}".format(
                machine.getWorkingOnBatch().getCode()))
        outputFile.write("\n")

    def printBatchState(self, batch, outputFile):
        currentBatchState = self.findStringRepresentationOfBatchState(batch)
        outputFile.write(
            "Batch {0:d} - state: {1:s} \n".format(batch.getCode(), currentBatchState))

    def findStringRepresentationOfBatchState(self, batch):
        if batch.getState() == 0:
            return "Has not joined the simulation"
        elif batch.getState() == 1:
            return "In buffer"
        elif batch.getState() == 2:
            return "In machine"
        elif batch.getState() == 3:
            return "Finished"

    def printSchedule(self, simulator, outputFile):
        outputFile.write("schedule: \n")
        for event in simulator.getSchedule().getSchedule():
            self.printEvent(event, outputFile)

    def printExecution(self, simulator, outputFile):
        try:
            outputFile = open(outputFile, "w")
        except:
            sys.stderr.write("Unable to open file {0:s}\n".format(outputFile))
            sys.stderr.flush()
            return

        outputFile.write("The events in the simulation:\n")
        for event in simulator.getExecution():
            self.printEvent(event, outputFile)

    def printEvent(self, event, outputFile):
        outputFile.write("event {0:d} at {1:f}: ".format(
            event.getNumber(), event.getDate()))

        if event.getType() == Event.BATCH_ENTERS_FIRST_BUFFER:
            outputFile.write("batch {0:d} enters the first buffer\n".format(
                event.getBatch().getCode()))
        elif event.getType() == Event.BATCH_ENTERS_BUFFER:
            outputFile.write("batch {0:d} unloads from machine {1:s} to buffer {2:s}\n".format(
                event.getBatch().getCode(), event.getTask().getMachine().getName(), event.getTask().getOutputBuffer().getName()))
        elif event.getType() == Event.LOAD_MACHINE_FROM_BUFFER:
            outputFile.write("batch {0:d} loads to machine {1:s} from buffer {2:s}\n".format(
                event.getBatch().getCode(), event.getTask().getMachine().getName(), event.getTask().getInputBuffer().getName()))
        elif event.getType() == Event.MACHINE_FINISHED_OPERATING_ON_BATCH:
            outputFile.write("batch {0:d} is finished processed by machine {1:s}\n".format(
                event.getBatch().getCode(), event.getTask().getMachine().getName()))

    def printAllSimulationsToTerminal(self, optimizer):
        simulationsDict = optimizer.getSimulations()
        print("simulations dict  :", simulationsDict)
        self.pretty(simulationsDict, 0)
        print("The best simulator was {0:s} with the time {1:f}".format(
            optimizer.getBestSimulation(), optimizer.getQuickestTime()))

    def pretty(self, d, indent):
        for key, value in d.items():
            print('\t' * indent + str(key))
            if isinstance(value, dict):
                self.pretty(value, indent+1)
            else:
                print('\t' * (indent+1) + str(value))


class HTMLPrinter:
    def __init__(self, plant):
        self.plant = plant
        self.simulations = None

    def generateReport(self, optimizer, fileName):
        self.simulations = optimizer.getSimulations()
        try:
            file = open(fileName, "w")
        except:
            print("Unable to open file {0:s}".format(fileName))
            return
        file.write("""<!DOCTYPE html>
<html>
<head>
<title>Simulation and Optimization of Wafer Production</title>
</head>
<body>""")
        file.write("<h1>Simulation and Optimization of Wafer Production</h1>\n")
        for simulation in self.simulations:
            self.printSimulation(simulation, file)

        file.write("""<h2>The best simulator was {0:s} with the time {1:d} seconds</h2>""".format(
            optimizer.getBestSimulation(), int(optimizer.getQuickestTime())))
        self.printSimulation(optimizer.getBestSimulation(), file)
        file.write("""</body>
</html>""")
        file.flush()
        file.close()

    def printSimulation(self, simulation, file):
        file.write("<h2>{0:s}</h2>\n".format(simulation))
        file.write(
            "<p>The parameters used in this simulations is described in the following table.</p>\n")
        file.write('<table>\n')
        stringMachineLogic = self.findStringRepresentationMachineLogic(
            self.simulations[simulation]["machineLogic"])
        stringBatchIntroduceLogic = self.findStringRepresentationBatchIntroduceLogic(
            self.simulations[simulation]["batchIntroduceLogic"])
        self.printTableRow("Machine task choosing logic",
                           stringMachineLogic, file)
        self.printTableRow("Batch introduction logic",
                           stringBatchIntroduceLogic, file)
        self.printTableRow("Batch size", str(
            self.simulations[simulation]["batchSize"]), file)
        self.printTableRow("Running time", str(
            self.simulations[simulation]["timeToSimulate"]), file)
        self.printTableRow("Batches Made", str(
            self.simulations[simulation]["batchesMade"]), file)
        file.write('</table>\n')

    def printTableRow(self, description, value, file):
        file.write("<tr>\n")
        file.write("  <td>{0:s}</td>\n".format(description))
        file.write("  <td>{0:s}</td>\n".format(value))
        file.write("</tr>\n")

    def findStringRepresentationMachineLogic(self, value):
        if value == 1:
            return "Chronological task selection"
        elif value == 2:
            return "Reverse Chronological task selection"
        elif value == 3:
            return "Choose buffer with longest queue"

    def findStringRepresentationBatchIntroduceLogic(self, value):
        if value == 1:
            return "Loaded when space in first buffer"


if __name__ == "__main__":
    # __________________________Task 1 - Plant design______________________________
    testPlant = Plant("testPlant")
    machine1 = testPlant.newMachine("1")
    machine2 = testPlant.newMachine("2")
    machine3 = testPlant.newMachine("3")
    # implemented a 'machine' that represents the final inventory
    finishedGoods = testPlant.newMachine("4")

    buffer1 = testPlant.newBuffer("1", 120, machine1)
    buffer2 = testPlant.newBuffer("2", 120, machine2)
    buffer3 = testPlant.newBuffer("3", 120, machine1)
    buffer4 = testPlant.newBuffer("4", 120, machine3)
    buffer5 = testPlant.newBuffer("5", 120, machine2)
    buffer6 = testPlant.newBuffer("6", 120, machine1)
    buffer7 = testPlant.newBuffer("7", 120, machine2)
    buffer8 = testPlant.newBuffer("8", 120, machine3)
    buffer9 = testPlant.newBuffer("9", 120, machine1)
    finalBuffer = testPlant.newBuffer(
        "finished inventory", 100000000000, finishedGoods)

    task1 = testPlant.newTask("1", machine1, buffer1, buffer2, 2, 0.5)
    task2 = testPlant.newTask("2", machine2, buffer2, buffer3, 2, 3.5)
    task3 = testPlant.newTask("3", machine1, buffer3, buffer4, 2, 1.2)
    task4 = testPlant.newTask("4", machine3, buffer4, buffer5, 2, 3)
    task5 = testPlant.newTask("5", machine2, buffer5, buffer6, 2, 0.8)
    task6 = testPlant.newTask("6", machine1, buffer6, buffer7, 2, 0.5)
    task7 = testPlant.newTask("7", machine2, buffer7, buffer8, 2, 1)
    task8 = testPlant.newTask("8", machine3, buffer8, buffer9, 2, 1.9)
    task9 = testPlant.newTask("9", machine1, buffer9, finalBuffer, 2, 0.3)
    printer = Printer(testPlant)
    print("How the plant looks like without any batches in it:   \n")
    printer.printPlantState("howThePlantLooks.txt")

    # ____________________________________Task 2  - Simulator design_______________________

    schedule = Schedule(testPlant)
    simulator = Simulator(testPlant, schedule)
    simulator.setMachineTaskChoosingLogic(Machine.CHRONOLOGICAL_TASK_SELECTION)

    # To test the Task 2, we have to load batches "by hand" in the system and see how it evolves.
    # the method "SimulationHardStart()" is added to start the simulation when the events are hard-coded
    # This functionality is later replaced with simulationLoop

    testBatch20 = testPlant.newBatch(20, 1)
    testBatch30 = testPlant.newBatch(30, 2)
    testBatch50 = testPlant.newBatch(50, 3)
    event1 = schedule.scheduleEvent(
        Event.BATCH_ENTERS_FIRST_BUFFER, 2, testBatch20, testPlant.findFirstTask())
    event2 = schedule.scheduleEvent(
        Event.BATCH_ENTERS_FIRST_BUFFER, 4, testBatch30, testPlant.findFirstTask())
    event3 = schedule.scheduleEvent(
        Event.BATCH_ENTERS_FIRST_BUFFER, 8, testBatch50, testPlant.findFirstTask())

    simulator.simulationHardCodeStart()
    printer.printExecution(simulator, "evolutionOfSystemHardCoded.txt")
    # printer.printExecution(simulator, sys.stdout)
    # It is also possible to run the simulation by starting a loop, the first argument is number of total wafers, and second is batchSize
    testPlant.resetPlant()
    schedule2 = Schedule(testPlant)
    simulator2 = Simulator(testPlant, schedule2)
    simulator2.setMachineTaskChoosingLogic(
        Machine.CHOOSE_BUFFER_WITH_MOST_BATCHES)
    simulator2.setIntroduceNewBatchesLogic(
        Simulator.LOAD_BATCHES_WHEN_MORE_SPACE_IS_AVAILABLE_IN_FIRST_BUFFER)
    simulator2.simulationLoop(200, 20)

    # printer.printExecution(simulator2, sys.stdout)
    # printer.printPlantState(sys.stdout)

    # _____________________________________Task 3 - Optimization design______________________-
    optimizer = Optimizer(testPlant, 1000)
    optimizer.startOptimization()
    printer.printAllSimulationsToTerminal(optimizer)
    htmlPrinter = HTMLPrinter(testPlant)
    htmlPrinter.generateReport(optimizer, 'report.html')
