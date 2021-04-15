
from WaferProductionTest import*


class AdditionalTableHTMLPrinter:
    def __init__(self, plant):
        self.plant = plant
        self.simulations = None

    def generateTable(self, optimizer, fileName):
        self.simulations = optimizer.getSimulations()
        try:
            file = open(fileName, "w")
        except:
            print("Unable to open file {0:s}".format(fileName))
            return
        file.write("""<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  overflow:hidden;padding:10px 5px;word-break:normal;}
.tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-x9e7{background-color:#c0c0c0;border-color:#000000;font-family:"Times New Roman", Times, serif !important;;font-size:15px;
  text-align:left;vertical-align:top}
.tg .tg-fhng{background-color:#c0c0c0;border-color:#000000;font-family:"Times New Roman", Times, serif !important;;text-align:left;
  vertical-align:top}
.tg .tg-xezz{background-color:#C0C0C0;border-color:#000000;font-family:"Times New Roman", Times, serif !important;;font-size:15px;
  text-align:left;vertical-align:top}
.tg .tg-bfjk{background-color:#c0c0c0;border-color:#000000;font-family:"Times New Roman", Times, serif !important;;font-size:14px;
  text-align:left;vertical-align:top}
.tg .tg-6pe1{background-color:#dae8fc;border-color:#000000;font-family:"Times New Roman", Times, serif !important;;font-size:24px;
  text-align:center;vertical-align:top}
.tg .tg-5mvr{background-color:#656565;border-color:#000000;color:#000000;font-family:"Times New Roman", Times, serif !important;;
  font-size:15px;text-align:left;vertical-align:top}
.tg .tg-gwr6{background-color:#c0c0c0;border-color:#000000;font-family:"Times New Roman", Times, serif !important;;font-size:16px;
  text-align:left;vertical-align:top}
.tg .tg-u1me{background-color:#656565;border-color:#000000;color:#000000;font-family:"Times New Roman", Times, serif !important;;
  font-size:14px;text-align:left;vertical-align:top}
.tg .tg-l6o9{background-color:#656565;border-color:#000000;font-family:"Times New Roman", Times, serif !important;;font-size:15px;
  text-align:center;vertical-align:top}
.tg .tg-0j94{background-color:#ffffff;border-color:#000000;font-family:"Times New Roman", Times, serif !important;;font-size:15px;
  text-align:left;vertical-align:top}
.tg .tg-iazv{background-color:#ffffff;border-color:#000000;font-family:"Times New Roman", Times, serif !important;;text-align:left;
  vertical-align:top}
</style>
<table class="tg">
<thead>
  <tr>
    <th class="tg-6pe1" colspan="8">Simulation Example</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-5mvr" colspan="2">Machine Choosing Logic</td>
    <td class="tg-gwr6" colspan="2">Chronological</td>
    <td class="tg-gwr6" colspan="2">Reverse Chronological</td>
    <td class="tg-fhng" colspan="2">Biggest Queue</td>
  </tr>
  <tr>
    <td class="tg-u1me" colspan="2">Batch introduction logic</td>
    <td class="tg-xezz" colspan="2">When space available</td>
    <td class="tg-xezz" colspan="2">When space available</td>
    <td class="tg-xezz" colspan="2">When space available</td>
  </tr>""")
        simulationNumber = 1
        firstRow = True
        for batchSize in optimizer.getBatchTypes():
            if firstRow:
                file.write("""<tr> 
                <td class="tg-l6o9" rowspan="4"><span style="color:#000">Batch Size</span></td>
    <td class="tg-bfjk">{0:d}</td>""".format(batchSize))
                firstRow = False
            else:
                file.write(""" <tr> 
    <td class="tg-bfjk">{0:d}</td>""".format(batchSize))
            for i in optimizer.getMachineTaskChoosingLogics():
                for j in optimizer.getIntroduceNewBatchesLogic():
                    file.write("""<td class="tg-iazv" colspan="2" style="text-align:center">{0:d}</td> """.format(int(
                        optimizer.getSimulations()["simulation: "+str(simulationNumber)]["timeToSimulate"])))
                    simulationNumber += 1
            file.write("""</tr> """)

        file.write("""</tbody>
</table> """)
        file.flush()
        file.close()


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


optimizer = Optimizer(testPlant, 1000)
optimizer.startOptimization()
htmlPrinter = AdditionalTableHTMLPrinter(testPlant)
htmlPrinter.generateTable(optimizer, 'tableReport.html')
