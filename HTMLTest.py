"""<style type = "text/css" >
.tg  {border-collapse: collapse
border-spacing: 0
}
.tg td{border-color: black
border-style: solid; border-width: 1px; font-family: Arial, sans-serif; font-size: 14px
  overflow: hidden; padding: 10px 5px; word-break: normal;}
.tg th{border-color: black
border-style: solid; border-width: 1px; font-family: Arial, sans-serif; font-size: 14px
  font-weight: normal; overflow: hidden; padding: 10px 5px; word-break: normal;}
.tg .tg-x9e7{background-color:  # c0c0c0;border-color:#000000;font-family:"Times New Roman", Times, serif !important;;font-size:15px;
  text-align: left
vertical-align: top}
.tg .tg-v40l{background-color:  # 9b9b9b;border-color:#000000;font-family:"Times New Roman", Times, serif !important;;font-size:15px;
  text-align: center
vertical-align: top}
.tg .tg-fhng{background-color:  # c0c0c0;border-color:#000000;font-family:"Times New Roman", Times, serif !important;;text-align:left;
             vertical-align: top}
.tg .tg-xezz{background-color:  # C0C0C0;border-color:#000000;font-family:"Times New Roman", Times, serif !important;;font-size:15px;
  text-align: left
vertical-align: top}
.tg .tg-bfjk{background-color:  # c0c0c0;border-color:#000000;font-family:"Times New Roman", Times, serif !important;;font-size:14px;
  text-align: left
vertical-align: top}
.tg .tg-hnok{background-color:  # ffffff;border-color:#000000;font-family:"Times New Roman", Times, serif !important;;font-size:24px;
  text-align: center
vertical-align: top}
.tg .tg-yj95{background-color:  # 9b9b9b;border-color:#000000;color:#000000;font-family:"Times New Roman", Times, serif !important;;
  font-size: 15px
text-align: left
vertical-align: top}
.tg .tg-gwr6{background-color:  # c0c0c0;border-color:#000000;font-family:"Times New Roman", Times, serif !important;;font-size:16px;
  text-align: left
vertical-align: top}
.tg .tg-mxzs{background-color:  # 9b9b9b;border-color:#000000;color:#000000;font-family:"Times New Roman", Times, serif !important;;
  font-size: 14px
text-align: left
vertical-align: top}
.tg .tg-0j94{background-color:  # ffffff;border-color:#000000;font-family:"Times New Roman", Times, serif !important;;font-size:15px;
  text-align: left
vertical-align: top}
.tg .tg-iazv{background-color:  # ffffff;border-color:#000000;font-family:"Times New Roman", Times, serif !important;;text-align:left;
             vertical-align: top}
</style >
<table class = "tg" >
<thead >
   <tr >
        <th class = "tg-hnok" colspan = "8" > Simulation Example < /th >
    </tr >
</thead >
<tbody >
   <tr >
        <td class = "tg-yj95" colspan="2">Machine Choosing Logic</td>
        <td class = "tg-gwr6" colspan="2">Chronological</td>
        <td class = "tg-gwr6" colspan="2">Reverse Chronological</td>
        <td class = "tg-fhng" colspan="2">Biggest Queue</td>
    </tr >
    <tr >
        <td class = "tg-mxzs" colspan="2">Batch introduction logic</td>
        <td class = "tg-x9e7">1st Load</td>
        <td class = "tg-x9e7">2nd load</td>
        <td class = "tg-xezz">1st Load</td>
        <td class = "tg-xezz">2nd load</td>
        <td class = "tg-xezz">1st Load</td>
        <td class = "tg-xezz">2nd load</td>
    </tr >
    <tr >
        <td class = "tg-v40l" rowspan="4">Batch Size</td>
        <td class = "tg-bfjk">20</td>
        <td class = "tg-0j94">data</td>
        <td class = "tg-0j94">data</td>
        <td class = "tg-0j94">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
    </tr >
    <tr >
        <td class = "tg-bfjk">25</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
    </tr >
    <tr >
        <td class = "tg-bfjk">40</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
    </tr >
    <tr >
        <td class = "tg-bfjk">50</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
    </tr >
</tbody >
</table > <style type="text/css">
.tg  {border-collapse: collapse
border-spacing:0
}
.tg td{border-color:black
border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px
  overflow: hidden; padding:10px 5px;word-break:normal;}
.tg th{border-color:black
border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px
  font-weight: normal; overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-x9e7{background-color:  # c0c0c0;border-color:#000000;font-family:"Times New Roman", Times, serif !important;;font-size:15px;
  text-align: left
vertical-align: top}
.tg .tg-v40l{background-color:  # 9b9b9b;border-color:#000000;font-family:"Times New Roman", Times, serif !important;;font-size:15px;
  text-align: center
vertical-align: top}
.tg .tg-fhng{background-color:  # c0c0c0;border-color:#000000;font-family:"Times New Roman", Times, serif !important;;text-align:left;
             vertical-align: top}
.tg .tg-xezz{background-color:  # C0C0C0;border-color:#000000;font-family:"Times New Roman", Times, serif !important;;font-size:15px;
  text-align: left
vertical-align: top}
.tg .tg-bfjk{background-color:  # c0c0c0;border-color:#000000;font-family:"Times New Roman", Times, serif !important;;font-size:14px;
  text-align: left
vertical-align: top}
.tg .tg-hnok{background-color:  # ffffff;border-color:#000000;font-family:"Times New Roman", Times, serif !important;;font-size:24px;
  text-align: center
vertical-align: top}
.tg .tg-yj95{background-color:  # 9b9b9b;border-color:#000000;color:#000000;font-family:"Times New Roman", Times, serif !important;;
  font-size: 15px
text-align:left
vertical-align:top}
.tg .tg-gwr6{background-color:  # c0c0c0;border-color:#000000;font-family:"Times New Roman", Times, serif !important;;font-size:16px;
  text-align: left
vertical-align: top}
.tg .tg-mxzs{background-color:  # 9b9b9b;border-color:#000000;color:#000000;font-family:"Times New Roman", Times, serif !important;;
  font-size: 14px
text-align:left
vertical-align:top}
.tg .tg-0j94{background-color:  # ffffff;border-color:#000000;font-family:"Times New Roman", Times, serif !important;;font-size:15px;
  text-align: left
vertical-align: top}
.tg .tg-iazv{background-color:  # ffffff;border-color:#000000;font-family:"Times New Roman", Times, serif !important;;text-align:left;
             vertical-align: top}
</style >
<table class = "tg">
<thead >
   <tr >
        <th class = "tg-hnok" colspan="8">Simulation Example</th>
    </tr >
</thead >
<tbody >
   <tr >
        <td class = "tg-yj95" colspan="2">Machine Choosing Logic</td>
        <td class = "tg-gwr6" colspan="2">Chronological</td>
        <td class = "tg-gwr6" colspan="2">Reverse Chronological</td>
        <td class = "tg-fhng" colspan="2">Biggest Queue</td>
    </tr >
    <tr >
        <td class = "tg-mxzs" colspan="2">Batch introduction logic</td>
        <td class = "tg-x9e7">1st Load</td>
        <td class = "tg-x9e7">2nd load</td>
        <td class = "tg-xezz">1st Load</td>
        <td class = "tg-xezz">2nd load</td>
        <td class = "tg-xezz">1st Load</td>
        <td class = "tg-xezz">2nd load</td>
    </tr >
    <tr >
        <td class = "tg-v40l" rowspan="4">Batch Size</td>
        <td class = "tg-bfjk">20</td>
        <td class = "tg-0j94">data</td>
        <td class = "tg-0j94">data</td>
        <td class = "tg-0j94">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
    </tr >
    <tr >
        <td class = "tg-bfjk">25</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
    </tr >
    <tr >
        <td class = "tg-bfjk">40</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
    </tr >
    <tr >
        <td class = "tg-bfjk">50</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
        <td class = "tg-iazv">data</td>
    </tr >
</tbody >
</table >"""
