var toggle = false;
var mydata;
var mywireless;
var locus = "Server1";
var migrating = false;
var pos1 = 0;
var id_last_item = 0;
var cont = 5;
var chart_remove_control = false;
var old_rx_b = 0;
var old_tx_b = 0;
var old_txfail_b = 0;
var containerTimer;
var dataSet;
var array_rx_bytes = [];
var array_tx_bytes = [];
var array_tx_failed = [];
var array_signal_float = [];
var percorrido = 0;
var current_server = "";
var current_device = "";
var calloptical = 1;

var mylinks = [{//***********pra q isso
    "name": "Server2",
    "latency_median": Math.random()*40,
    "latency_min": Math.random()*40,
    "latency_max": Math.random()*40,
    "jitter": Math.random()*3,
},
{
    "name": "Server3",
    "latency_median": Math.random()*40,
    "latency_min": Math.random()*40,
    "latency_max": Math.random()*40,
    "jitter": Math.random()*3,
},
{
    "name": "Server4",
    "latency_median": Math.random()*40,
    "latency_min": Math.random()*40,
    "latency_max": Math.random()*40,
    "jitter": Math.random()*3,
},
{
    "name": "Server5",
    "latency_median": Math.random()*40,
    "latency_min": Math.random()*40,
    "latency_max": Math.random()*40,
    "jitter": Math.random()*3,
}];

var dashboardTimer;
var linksTimer;
var pollTime = 3000;

$(document).ready(function(){
    postDashboard();

    addBtnListeners();

    $("#modal-container-link").on('shown', function(){//shows links modal
        if(!linksTimer){
            clearTimeout(dashboardTimer);
            dashboardTimer = null;//stops dashboard pooling

            $("#myModalLabel").html(locus+" Network Links");//starts links data pooling
            id_last_item = 0;
            current_server = "";
            requestlinksData();
            
        }
    });

    $("#modal-container-link").on('hidden', function(){//shows dashboard links when modal is closed
        clearTimeout(linksTimer);
        linksTimer = null;

        postDashboard();
    });

});

function postDashboard(){//posts dashboard servers data
    //console.log("Dashboard!");
    $.ajax({
        url: "/REST/network/dashboard", 
        dataType: 'json',
        success: function(result){
            //console.log(JSON.stringify(result));
            mydata = result["data"];

            clearServers();
            addServers(mydata);

            dashboardTimer = setTimeout(postDashboard, pollTime);
        },
        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr.status);
            console.log(thrownError);
        }
    });
}



function requestlinksData(){
    console.log("Links!"); //quando a função é iniciada corretamente, essa mensagem é printada no console
     console.log("locus: "+locus);//printa o locus no console
    // console.log("My ID:"+id_last_item);

    $.ajax({// é o uso do objeto XMLHttpRequest para se comunicar com os scripts do lado do servidor. Recebe informações no formato JSON
        url: "/REST/network/dashboardlinks/", //url específica para mandar o request (busca a o JSON nessa url)
        dataType: 'json',//especifica o tipo de dado esperado da resposta do servidor
        data: {//especifica o dado mandado ao servidor
            locus: locus,
            id_last_item:  id_last_item,
        },

        success: function(result) { //função que roda quando a comunicação com o servidor da certo
            console.log(JSON.stringify(result));//expoe a lista no console
            // console.log(result["links"]);
           
           //verifica se o result["links"] possui algum elemento (se existe)

            if(typeof result["error"] === 'undefined') {// does not exist

                // Pegar do horário atual
               /* var timestamp = new Date().toLocaleString();
                console.log("TIMESTAMP ATUAL: "+timestamp);*/
                if (calloptical){
                    if (result["links"].length !== 0){//testa se a lista está vazia
                        $('#optical-bord').show();
                        
                        var flag = 0; //vai zerar sempre no inicio
                        var pos = 0;
                        
                        /**** ALL TABLE - OPTICAL*******/
                        if (current_server == ""){
                            $('#all_optical_tab').click(function (e){
                                e.preventDefault();
                                current_server = "table_all_optical";
                                id_last_item=0;
                                flag = 0;
                            });
                            $( "#5points" ).click(function() {
                                if (cont > 5){
                                    chart_remove_control = true;
                                }
                                    cont = 5;
                            });

                           $( "#10points" ).click(function() {
                               if (cont > 10){
                                    chart_remove_control = true;
                                }
                                cont = 10;
                            });

                            $( "#20points" ).click(function() {
                                if (cont > 20){
                                    chart_remove_control = true;
                                }
                                cont = 20;
                            });
                        }
                        for(i=0; i<(result["links"].length); i++){//percorre o json
                           
                            if (current_server == ""){ //testa se o json ja foi percorrido mais de uma vez
                                
                                if(i==0){
                                    $('#tab-list li[role="presentation"]').remove();
                                    $('#tab-list').append($('<li role="presentation" class="active"><a id="' +result["links"][i]["name"]+ '_tab" class="tab_link" href="#to_server" "aria-controls="to_server_' +result["links"][i]["name"]+ '" role="tab" data-toggle="tab">to ' +result["links"][i]["name"]+ ' </a></li>"'))
                                }
                                else 
                                    $('#tab-list').append($('<li role="presentation"><a id="' +result["links"][i]["name"]+ '_tab" class="tab_link" href="#to_server" "aria-controls="to_server_' +result["links"][i]["name"]+ '" role="tab" data-toggle="tab">to ' +result["links"][i]["name"]+ ' </a></li>"'))
                                    
                                $('#'+result["links"][i]["name"]+'_tab').click(function (event){
                                    event.preventDefault();
                                    current_server = event.target.id.toString().split("_tab")[0];
                                    console.log("Current_server-> " + current_server);
                                    clearOpticalData(0);
                                    id_last_item=0;
                                    flag = 0;
                                    clearTimeout(linksTimer);
                                    calloptical = 1;
                                    requestlinksData();
                                }); 

                                if (current_server == "" && i==result["links"].length-1){
                                    current_server = result["links"][0]["name"];//define variavel como o servidor a ser monitorado
                                    pos = 0;
                                    flag++;
                                    calloptical=1;
                                }
                            } 

                            else {           
                                if(result["links"][i]["name"] == current_server){ //procura pelo nome "Server2"
                                    // console.log("CURRENT SERVER WAS FOUND -> " + current_server);
                                    pos = i;//variavel que guarda a posição do array em que os links desse Server2 estao
                                    // console.log("POS: " +pos);
                                    flag++;//incrementa o flag pra entrar no if que vai desenhar o gráfico so com os dados do server 2
                                    calloptical=1;
                                }
                            }
                        }

                            
                        if (flag !=0 && current_server != "table_all_optical"){
                            //clear series data
                            if(chart_remove_control){
                                clearOpticalData(cont);
                                chart_remove_control = false;
                            }

                            plotChartJitterLatency(result,pos);
                            flag = 0;
                            calloptical = 1;

                            // console.log("ID received:"+result["id_last_item"]);
                            
                            id_last_item = result["id_last_item"]; //salva o id do ultimo item
                        } 

                        else if (current_server == "table_all_optical"){
                            plotTableAllOptical(result);
                            flag++;
                            calloptical=1;
                        }                     

                    

                        else if (current_server == "")
                            $('#optical-bord').hide();
                    } 
                }
                 
                //WIRELESS
                if(typeof result["wireless"] !== 'undefined') {
                   
                    //console.log("Wireless-> " + result["wireless"][0] + "aaana " + result["wireless"].length);

                    if (result["wireless"] != null && result["wireless"].length > 0 && result["wireless"][0] != null){//testa se a lista está vazia

                        $('#wireless-bord').show();
                        
                        for(i=0; i<result["wireless"].length; i++){//percorre o json

                            if(current_device == ""){//testa se o json ja foi percorrido
                                
                                /*$('#all_wireless_tab').click(function (e){
                                e.preventDefault();
                                current_device = "table_all_wireless";
                                //plotTableAllWireless(result);
                                
                                calloptical = 0;
                                });*/

                                pos1=0;
                                var id_mac = result["wireless"][i]["mac"].replace(/:/g, "");
                                console.log("id mac: "+i+'_'+id_mac);

                                if(i==0){ //define a primeira tab como active
                                    $('#wireless-tab-list li[role="presentation"]').remove();
                                    $('#wireless-tab-list').append($('<li role="presentation" class="active"><a id="'+i+'_'+id_mac+'" class="tab_link" href="#device_" "aria-controls="device' +i+ '" role="tab" data-toggle="tab">Device '+(i+1)+ ' </a></li>"'))
                                }
        
                                else 
                                    $('#wireless-tab-list').append($('<li role="presentation"><a id="'+i+'_'+id_mac+'" class="tab_link" href="#device_" "aria-controls="device' +i+ '" role="tab" data-toggle="tab">Device ' +(i+1)+ ' </a></li>"'))    
                                
                                console.log('device'+(i+1)+' mac: ' +result["wireless"][i]["mac"]);

                                $('#'+i+'_'+id_mac).click(function (event){//se alguma tab for clicada, define essa tab como current_device e a posicao em que esta no array
                                    event.preventDefault();
                                    current_device = event.target.id.toString();
                                    pos1= current_device.split("_")[0];
                                    console.log("Current_device-> " + current_device +" Pos1: "+pos1);
                                    id_last_item=0;
                                    flag = 0;
                                    calloptical = 0;
                                    clearTimeout(linksTimer);
                                    requestlinksData();
                                }); 


                                if (current_device == "" &&  i==result["wireless"].length-1 && current_device !== "table_all_wireless"){//se todas as tabs ja foram criadas, define o current_device como a primeira tab e define a sua posicao como o primeiro elemento do array
                                    pos1 = 0;
                                    current_device = pos1+'_'+result["wireless"][0]["mac"].replace(/:/g, "");//define variavel como o servidor a ser monitorado
                                    calloptical=0;    
                                }

                                else if (current_device == "table_all_wireless"){
                                    
                                   
                                    calloptical=0;
                                    console.log("ALL TABLE WIRELESS CLICKED.");
                                }

                                console.log("RESULT: "+result["wireless"][pos1]["mac"]);

                            }
                        }

                        
                        console.log("POS: "+pos1);
                        console.log("estou aqui! Current_device: "+current_device );

                        //definimos um array de dados da lista para cada uma das variaveis
                        if(result["wireless"][pos1] != null && current_device !== "table_all_wireless"){
                            

                            var signal = result["wireless"][pos1]["signal"];//recebe o sinal como uma string
                            var rx_bytes = result["wireless"][pos1]["rx_bytes"];
                            var tx_bytes = result["wireless"][pos1]["tx_bytes"];
                            var tx_failed = result["wireless"][pos1]["tx_failed"];
                            var mac = result["wireless"][pos1]["mac"];
                            var signal_slice = signal.slice(0,6);//pega o pedaço da string que contem o valor do sinal em dBm
                            var signal_float= parseFloat(signal_slice);//transforma a string para float

                            //console.log("WIRELESS 1: "+result["wireless"][1]["mac"]);

                            plotTableAllWireless(signal_float, tx_failed, tx_bytes, rx_bytes, mac);
                    
                            plotChartRxTx(tx_bytes, tx_failed, rx_bytes, mac);


                            plotChartSignal(signal_float);
                            flag = 0;
                            calloptical=0;
                        }    
                    }
                    else{
                        $('#wireless-bord').hide();
                    }
                }
                else{
                    $('#wireless-bord').hide();
                }

            }
            // call it again after one second 
            calloptical=1;
            linksTimer = setTimeout(requestlinksData, pollTime);
        },

        error: function(result) {//se não consegue se comunicar com o servidor 

            console.log("search link error!");
        },

        cache: false
    });
}



function plotChartJitterLatency(result, pos){
    var latency_up = (result["links"][pos]["latency_up"] < 0.1) ? 0.1 : result["links"][pos]["latency_up"];//if result < 0.1, 0.1; else val

    var latency_down = (result["links"][pos]["latency_down"] < 0.1) ? 0.1 : result["links"][pos]["latency_down"];
    var jitter_up = result["links"][pos]["jitter_up"];
    var jitter_down = result["links"][pos]["jitter_down"];
    
    
    // add the point
    for(var i = 0; i < latency_up.length; i++){
        var shift_latency_up = chart1.series[0].data.length >= cont; // shift if the series is longer than cont
        var shift_latency_down = chart1.series[1].data.length >= cont;
        var shift_jitter_up = chart2.series[0].data.length >= cont; // shift if the series is longer than cont
        var shift_jitter_down = chart2.series[1].data.length >= cont; 
        chart1.series[0].addPoint(latency_up[i], true, shift_latency_up);
        chart1.series[1].addPoint(latency_down[i], true, shift_latency_down);
        chart2.series[0].addPoint(jitter_up[i], true, shift_jitter_up);
        chart2.series[1].addPoint(jitter_down[i], true, shift_jitter_down);
    }

    if (chart1.series[0].data.length > cont || chart1.series[1].data.length > cont || chart2.series[0].data.length > cont || chart2.series[1].data.length > cont){
        clearOpticalData(cont);
    }
}



function clearOpticalData(remove_count){
    while(chart1.series[0].data.length > remove_count){
        chart1.series[0].data[0].remove();   
    }
    while(chart1.series[1].data.length > remove_count){
        chart1.series[1].data[0].remove();  
    }
    while(chart2.series[0].data.length > remove_count){
        chart2.series[0].data[0].remove();
    }
    while(chart2.series[1].data.length > remove_count){
        chart2.series[1].data[0].remove();   
    }
}


function plotTableAllOptical(result){
    var table = $('#table-optical').DataTable();
    while ( table.rows().count() > 0 ) {
        table.clear();
        table.draw();
    }
    
    for (i=0; i<result["links"].length; i++){   

        var sum_latency_up = 0.0;
        var sum_latency_down = 0.0;
        var sum_jitter_up = 0.0;
        var sum_jitter_down = 0.0;

        if (result["links"][i]["latency_up"].length>0){

            for(j=0; j<result["links"][i]["latency_up"].length; j++)
                sum_latency_up += result["links"][i]["latency_up"][j];

            var latency_up_value = sum_latency_up/result["links"][i]["latency_up"].length;
            var latency_up_media =  parseFloat(latency_up_value.toFixed(2));
        }
            
        if(result["links"][i]["latency_down"].length>0){

            for(j=0; j< result["links"][i]["latency_down"].length; j++)
                sum_latency_down += result["links"][i]["latency_down"][j];
            
            var latency_down_value = sum_latency_down/result["links"][i]["latency_down"].length;
            var latency_down_media = parseFloat(latency_down_value.toFixed(2));
        }
            
        if(result["links"][i]["jitter_up"].length>0){

            for(j=0; j<result["links"][i]["jitter_up"].length; j++)
                sum_jitter_up += result["links"][i]["jitter_up"][j];
          
            var jitter_up_value = sum_jitter_up/result["links"][i]["jitter_up"].length;                        
            var jitter_up_media = parseFloat(jitter_up_value.toFixed(2));

        }
        
        if(result["links"][i]["jitter_down"].length>0){    
            
            for(j=0; j<result["links"][i]["jitter_down"].length; j++)
                sum_jitter_down += result["links"][i]["jitter_down"][j];
            
            var jitter_down_value = sum_jitter_down/result["links"][i]["jitter_down"].length;
            var jitter_down_media = parseFloat(jitter_down_value.toFixed(2));
        }


        var dataSet = [result["links"][i]["name"], latency_up_media, latency_down_media, jitter_up_media, jitter_down_media];
        table.row.add(dataSet).draw();  
    }
}

function plotChartSignal(signal_float){
/****** CHARTSPEED *************/
    var point;

    if (chartSpeed) {
        point = chartSpeed.series[0].points[0];
        point.update(signal_float);
    }
}

function plotChartRxTx(tx_bytes, tx_failed, rx_bytes, mac){
    // add data
    var seriesData = [];
    seriesData.push(["TX", tx_bytes]);
    seriesData.push(["TX Failed", tx_failed]);
    seriesData.push(["RX", rx_bytes]);
    chart3.series[0].setData(seriesData, true);

    
    $("#mac_data").html("MAC: " +mac);
    $("#tx_failed_data").html("TX failed: " +tx_failed);
    $("#tx_bytes_data").html("TX: " +tx_bytes);
    $("#rx_bytes_data").html("RX: " +rx_bytes);

}

/*function plotTableAllWireless(result){
    var table = $('#table-wireless').DataTable();
    while ( table.rows().count() > 0 ) {
        table.clear();
        table.draw();
    }

    

    for (i=0; i<result["wireless"].length; i++){  
        console.log("TESTE: "+result["wireless"][i]["rx_bytes"].length); 

        var sum_rx_bytes = 0.0;
        var sum_tx_bytes = 0.0;
        var sum_tx_failed = 0.0;
        var sum_signal_float = 0.0;
        var j = 0;

        
        
        if (result["wireless"][i]["rx_bytes"].length>0){

            for(j=0; j<result["wireless"][i]["rx_bytes"].length; j++)
                sum_rx_bytes += result["wireless"][i]["rx_bytes"][j];

            var rx_bytes_value = sum_rx_bytes/result["wireless"][i]["rx_bytes"].length;
            var rx_bytes_media =  parseFloat(rx_bytes_value.toFixed(2));

        }

            
        if(result["wireless"][i]["tx_bytes"].length>0){

            for(j=0; j< result["wireless"][i]["tx_bytes"].length; j++)
                sum_tx_bytes += result["wireless"][i]["tx_bytes"][j];
            
            var tx_bytes_value = sum_tx_bytes/result["wireless"][i]["tx_bytes"].length;
            var tx_bytes_media = parseFloat(tx_bytes_value.toFixed(2));
        }
            
        if(result["wireless"][i]["tx_failed"].length>0){

            for(j=0; j<result["wireless"][i]["tx_failed"].length; j++)
                sum_tx_failed += result["wireless"][i]["tx_failed"][j];
          
            var tx_failed_value = sum_tx_failed/result["wireless"][i]["tx_failed"].length;                        
            var tx_failed_media = parseFloat(jitter_up_value.toFixed(2));

        }
        
        if(result["wireless"][i]["signal"].length>0){    
            
            for(j=0; j<result["wireless"][i]["signal"].length; j++){
                var signal_table = result["wireless"][i]["signal"][j];
                var signal_slice_table = signal_table.slice(0,6);//pega o pedaço da string que contem o valor do sinal em dBm
                var signal_float_table= parseFloat(signal_slice_table);//transforma a string para float
                array_signal_float.push(signal_float_table);
                sum_signal_float += signal_float_table;
            }
            
            var signal_value = sum_signal_float/result["wireless"][i]["signal"].length;
            var signal_media = parseFloat(signal_value.toFixed(2));
        }


        var dataSet = ["Device"+(i+1),result["wireless"][i]["mac"],rx_bytes_media, tx_bytes_media, tx_failed_media, signal_media];
        table.row.add(dataSet).draw();
        /*var dataSetWireless = ["Device"+(i+1),result["wireless"][i]["mac"],rx_bytes_media, tx_bytes_media, tx_failed_media, signal_media];
        table.row.add(dataSetWireless).draw(); 
    }


}
*/


function plotTableAllWireless(signal_float, tx_failed, tx_bytes, rx_bytes, mac){

      
        //ALL TABLE WIRELESS
        var sum_rx_bytes = 0.0;
        var sum_tx_bytes = 0.0;
        var sum_tx_failed = 0.0;
        var sum_signal = 0.0;

        array_rx_bytes.push(rx_bytes);
        array_tx_bytes.push(tx_bytes);
        array_tx_failed.push(tx_failed);
        array_signal_float.push(signal_float);

        
            
            for(i=0; i<array_rx_bytes.length; i++)
                sum_rx_bytes += parseFloat(array_rx_bytes[i]);
        

            var rx_bytes_value = sum_rx_bytes/array_rx_bytes.length;
            var rx_bytes_media = parseFloat(rx_bytes_value.toFixed(2));
       
            
            for(i=0; i<array_tx_bytes.length; i++)
                sum_tx_bytes += parseFloat(array_tx_bytes[i]);
            
            var tx_bytes_value = sum_tx_bytes/array_tx_bytes.length;
            var tx_bytes_media = parseFloat(tx_bytes_value.toFixed(2));
            
            for(i=0; i<array_tx_failed.length; i++)
                sum_tx_failed += parseFloat(array_tx_failed[i]);
            
            var tx_failed_value = sum_tx_failed/array_tx_failed.length;                        
            var tx_failed_media = parseFloat(tx_failed_value.toFixed(2));

            for(i=0; i<array_signal_float.length; i++)
                sum_signal += parseFloat(array_signal_float[i]);
            
            var signal_value = sum_signal/array_signal_float.length;
            var signal_media = parseFloat(signal_value.toFixed(2));



    var dataSet = ["Device 1", mac, rx_bytes_media, tx_bytes_media, tx_failed_media, signal_media];
    var table2 = $('#table-wireless').DataTable();
    
    while ( table2.rows().count() > 0 ) {
        table2.clear();
        table2.draw();
    }

    table2.row.add(dataSet).draw();   
    
}


function addServers(servers){
    var main = $("#dashboard-main");
    var row;

    for(var i = 0; i < servers.length; i++){
        if( i % 3 == 0){
            if(typeof row !== "undefined"){
                $(main).append(row);
            }

            row = $("<div>",{class: "row server-data"});
        }

        colmd4 = $("<div>",{class: "col-md-4"});
        $(colmd4).append(createPanel(servers[i]));
        $(row).append(colmd4);
    }

    if(servers.length != 0){
        $(main).append(row);
    }


    $(".link-btn").click(function(){
        locus = $(this).attr("name");
    });

    $(".container-app").on('mouseenter', function(){
        showContainerActions(this);
        $(".container-actions").mouseleave(function() {
            containerTimer = setTimeout(hideContainerActions, 10);
        }).mouseenter(function() {
            clearTimeout(containerTimer);
        });
    });

    $(".container-app").mouseleave(function() {
        containerTimer = setTimeout(hideContainerActions, 10);
    }).mouseenter(function() {
        clearTimeout(containerTimer);
    });
    
}

function clearServers(){
    $(".server-data").remove();
}

function createPanel(server){
    var panel = $("<div>", {class: "panel panel-primary"});
    var heading = $("<div>", {class: "panel-heading"});
    var body = createBody(server);
    var footer = $("<div>", {class: "panel-footer"});

    $(heading).append($("<h3>", {class: "panel-title"}).html(server.name))
    $(heading).append($("<button>",{
        class: "btn btn-default btn-geo"
    }).html($("<span>",{class: "glyphicon glyphicon-map-marker"})));

    $(footer).append($("<button>",{
        style: "width: 100%",
        id: "modal-link",
        href: "#modal-container-link",
        role: "button",
        class: "btn link-btn",
        "data-toggle": "modal",
        name: server.name
    }).html("Links"));

    $(panel).append(heading);
    $(panel).append(body);
    $(panel).append(footer);

    return panel;
}

function createBody(server){
    var body = $("<div>", {class: "panel-body"});
    var fixed_tp = parseFloat(server.throughput/1000).toFixed(2);

    $(body).append($("<span>").html("CPU"));
    $(body).append(createProgressBar(server.cpu));
    $(body).append($("<span>").html("Memory"));
    $(body).append(createProgressBar(server.mem));
    $(body).append($("<span>").html("Network load"));
    if(server.throughput != null)
        $(body).append($("<h2>").html(fixed_tp+" mbps"));
    else
        $(body).append($("<h2>").html("No data"));
    $(body).append($("<div>").html("Containers"));
    var group = $("<div>",{class: "container-app-group", server: server.name});

    if(server.containers.length > 0)
        for(var i = 0; i < server.containers.length; i++)
            $(group).append($("<span>", {id: server.containers[i]["name"]+i ,
                                        class: "badge badge-primary container-app",
                                        status: server.containers[i]["status"],
                                        draggable: true}).html(server.containers[i]["name"]));
    else
        $(group).append($("<small>").html("No data"));

    $(group).append($("<span>",{class: "badge btn-add-container"}).html("+"));

    if(migrating){
        var overlay = $("<div>",{class: "container-overlay"});
        $(group).addClass("container-migrating");
        $(group).append(overlay);
    }

    $(body).append(group);

    return body;
}

function createProgressBar(number){
    var fixed_number = parseFloat(number).toFixed(1);

    var div = $("<div>",{
        class: "progress"
    });
    var bar = $("<div>",{
        class: "progress-bar",
        role: "progressbar",
        style: "width: "+fixed_number+"%",
        "aria-valuenow": fixed_number,
        "aria-valuemin": 0,
        "aria-valuemax": 100,
    }).html(fixed_number+"%");

    $(div).append(bar);

    return div;
}

function addBtnListeners(){
    $("#btn-manual").click(function(){
        $(".btn-deleg").parent().removeClass("active");
        $(this).parent().addClass("active");

        var auto_delegation_type;
        var delegation_mode = "m";
        var message = "Success: Delegation changed to Manual!"

        $.ajax({
            url: "/REST/network/configuration/", 
            dataType: "json",
            method: "POST",
            data: {
                delegation_mode: delegation_mode,
                //auto_delegation_type: auto_delegation_type
            },
            success: function(result){
                //console.log(JSON.stringify(result));
                $("div.success").html(message);
                $( "div.success" ).fadeIn( 300 ).delay( 1500 ).fadeOut( 400 );
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        });
        
    });

    $("#btn-thresh-cpu").click(function(){
        $(".btn-deleg").parent().removeClass("active");
        $(this).parent().addClass("active");
        $(this).parent().parent().parent().addClass("active");

        var auto_delegation_type = "threshold_cpu";
        var delegation_mode = "a";
        var message = "Success: Delegation changed to Automatic - Threshold CPU!"

        $.ajax({
            url: "/REST/network/configuration/", 
            dataType: "json",
            method: "POST",
            data: {
                delegation_mode: delegation_mode,
                auto_delegation_type: auto_delegation_type
            },
            success: function(result){
                //console.log(JSON.stringify(result));
                $("div.success").html(message);
                $( "div.success" ).fadeIn( 300 ).delay( 1500 ).fadeOut( 400 );
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        });
        
    });

    $("#btn-thresh-lat").click(function(){
        $(".btn-deleg").parent().removeClass("active");
        $(this).parent().addClass("active");
        $(this).parent().parent().parent().addClass("active");

        var auto_delegation_type = "threshold_lat";
        var delegation_mode = "a";
        var message = "Success: Delegation changed to Automatic - Threshold Latency!"

        $.ajax({
            url: "/REST/network/configuration/", 
            dataType: "json",
            method: "POST",
            data: {
                delegation_mode: delegation_mode,
                auto_delegation_type: auto_delegation_type
            },
            success: function(result){
                console.log(JSON.stringify(result));
                $("div.success").html(message);
                $( "div.success" ).fadeIn( 300 ).delay( 1500 ).fadeOut( 400 );
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        });
        
    });

    $("#btn-thresh-cpulat").click(function(){
        $(".btn-deleg").parent().removeClass("active");
        $(this).parent().addClass("active");
        $(this).parent().parent().parent().addClass("active");

        var auto_delegation_type = "threshold_cpulat";
        var delegation_mode = "a";
        var message = "Success: Delegation changed to Automatic - Threshold CPU/Latency!"

        $.ajax({
            url: "/REST/network/configuration/", 
            dataType: "json",
            method: "POST",
            data: {
                delegation_mode: delegation_mode,
                auto_delegation_type: auto_delegation_type
            },
            success: function(result){
                console.log(JSON.stringify(result));
                $("div.success").html(message);
                $( "div.success" ).fadeIn( 300 ).delay( 1500 ).fadeOut( 400 );
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        });
        
    });
}

function showContainerActions(element){
    if(!ondragContainerId){
        var i;
        var position = $(element).offset();
        var actionLeft = position.left;
        var actionTop = $(element).outerHeight()+position.top;
        var buttons = [{
            type: "play",
            color: "#6BA368",
            action: "start"
        },{
            type: "play",
            color: "#6BA368",
            action: "unfreeze"
        },{
            type: "pause",
            color: "#70A9A1",
            action: "freeze"
        },{
            type: "stop",
            color: "#CC2936",
            action: "stop"
        },{
            type: "remove",
            color: "#CC2936",
            action: "delete"
        },{
            type: "console",
            color: "#3F4045",
            action: "terminal"
        }]

        var rectangule = $("<div>",{
            class: "container-actions",
            style: "left: "+actionLeft+";top:"+actionTop+";"
        });

        for(i = 0; i < buttons.length; i++){
            if(!($(element).attr("status") == "Running" && buttons[i].action == "start")
            && !($(element).attr("status") == "Running" && buttons[i].action == "delete") 
            && !($(element).attr("status") == "Running" && buttons[i].action == "unfreeze")
            && !($(element).attr("status") == "Stopped" && buttons[i].action == "stop")
            && !($(element).attr("status") == "Stopped" && buttons[i].action == "freeze")
            && !($(element).attr("status") == "Stopped" && buttons[i].action == "unfreeze")
            && !($(element).attr("status") == "Frozen" && buttons[i].action == "start")
            && !($(element).attr("status") == "Frozen" && buttons[i].action == "freeze")
            && !($(element).attr("status") == "Frozen" && buttons[i].action == "delete") ){
                rectangule.append($("<span>",{
                    class: "badge btn-container-action",
                    style: "background-color: "+buttons[i].color
                }).html($("<span>",{
                    class: "glyphicon glyphicon-"+buttons[i].type
                })).click({button: buttons[i],element: element},function(event){
                    var element = event.data.element;
                    var button = event.data.button;
                    console.log("Action: "+button.action);

                    if(button.action != "terminal"){
                        $.ajax({
                            method: "POST",
                            url: "/REST/container",
                            data: {
                                container_pool: $(element).parent().attr("server"),
                                container_name: $(element).html(),
                                operation: button.action
                            },
                            success: function(result){
                                //remove layer
                                console.log(JSON.stringify(result));
                                // migrating = false;
                            },
                            error: function (xhr, ajaxOptions, thrownError) {
                                console.log(xhr.status);
                                console.log(thrownError);
                            }
                        });
                    }
                    else{
                        window.open("/core/containers_list/"+button.action+"/"+$(element).parent().attr("server")+"/"+$(element).html());
                    }
                }));
            }
        }

        $("body").append(rectangule);
        $(".container-actions").slideDown();
    }
}

function hideContainerActions(element){
    $(".container-actions").slideUp(500, function(){
        $(this).remove();
    })
}

var ondragContainerId;

$("html").on("dragstart", function(event) {
    ondragContainerId = event.target.id;
    //console.log(ondragContainerId);
    hideContainerActions();

});

$("html").on("dragenter", function(event) {
    event.preventDefault();  
    event.stopPropagation();
    if($(event.target).hasClass("container-app-group")){
        $(event.target).addClass('container-group-hover');
    }

    if($(event.target).parent().hasClass("container-app-group")){
        $(event.target).parent().addClass('container-group-hover');
    }
});

$("html").on("dragover", function(event) {
    event.preventDefault();  
    event.stopPropagation();
    $(this).addClass('dragging');
    hideContainerActions();
});

$("html").on("dragleave", function(event) {
    event.preventDefault();  
    event.stopPropagation();
    $(this).removeClass('dragging');
    if($(event.target).hasClass("container-app-group")){
        $(event.target).removeClass('container-group-hover');
    }

    if($(event.target).parent().hasClass("container-app-group")){
        $(event.target).parent().removeClass('container-group-hover');
    }
});

$("html").on("drop", function(event) {
    event.preventDefault();
    event.stopPropagation();
    var appGroup;
    
    var container = $("#"+ondragContainerId);
    if($(event.target).parent().hasClass("container-app-group")){
        appGroup = $(event.target).parent()
    }
    else{
        appGroup = event.target;
    }

    if($(appGroup).hasClass("container-app-group")){
        
        var lastgroup = $(container).parent();

        $(container).remove();
        if($(lastgroup).children().length == 1){
            var lastplus = $(lastgroup).children().last();
            $("<small>").html("No data").insertBefore(lastplus);
        }
        $(appGroup).find("small").remove();
        var plus = $(appGroup).children().last();
        $(container).insertBefore(plus);

        //Remove Hover Effect
        $(appGroup).removeClass('container-group-hover');

        // console.log("Container name:"+$(container).html()+" ;Server Source:"+$(lastgroup).attr("server")+" ;Server dest:"+$(appGroup).attr("server")+" ;")
        containerMigrate($(container).html(),$(lastgroup).attr("server"),$(appGroup).attr("server"));
    }

    ondragContainerId = null;
});

function containerMigrate(name, src, dst){
    $.ajax({
        method: "POST",
        url: "/REST/container",
        data: {
            container_pool: src,
            container_name: name,
            operation: "migrate",
            destination_pool: dst
        },
        beforeSend: function(){
            migrating = true;
            var overlay = $("<div>",{class: "container-overlay"});
            $(".container-app-group").addClass("container-migrating");
            $(".container-app-group").append(overlay);
        },
        success: function(result){
            //remove layer
            console.log(JSON.stringify(result));
            migrating = false;
        },
        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr.status);
            console.log(thrownError);
        }
    });
}
