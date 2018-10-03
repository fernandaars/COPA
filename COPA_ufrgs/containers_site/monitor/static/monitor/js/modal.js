
$(document).ready(function() {
    $('#table-optical').DataTable( {
        data: dataSet,
        columns: [
            { title: "Links" },
            { title: "Latency Up" },
            { title: "Latency Down" },
            { title: "Jitter Up" },
            { title: "Jitter Down" }
        ],
        scrollY: 200,
        paging: false,
        "info": false,
        /*ajax: '/api/staff',
        rowId: 'staffId',*/
    } );

    $('#table-wireless').DataTable( {
        //data: dataSetWireless,
        data: dataSet,
        columns: [
            { title: "Devices" },
            { title: "MAC" },
            { title: "RX" },
            //{ title: "RX Failed" },
            { title: "TX" },
            { title: "TX Failed" },
            {title: "Signal"}
        ],
        "columns":[{ "defaultContent": "<i>Not set</i>"}],
        scrollY: 200,
        paging: false,
        "info": false,
        /*ajax: '/api/staff',
        rowId: 'staffId',*/
    } );

} );

// Disable search and ordering by default
$.extend( $.fn.dataTable.defaults, {
    searching: false,
} );

/*$(document).ready(function () {
    var tabID = 2;
    
    $('#btn-add-tab').click(function () {
        tabID++;
        //<li role="presentation" class="active"><a class="tab_link" href="#to_server_2" aria-controls="to_server_2" role="tab" data-toggle="tab">to Server 2</a></li>

        $('#tab-list').append($('<li role="presentation"><a class="tab_link" href="#to_server_"'  + tabID + ' "aria-controls="to_server_"' + tabID + '" role="tab" data-toggle="tab">to Server ' +tabID+ ' </a></li>"'));
        $('#tab-content').append($('<div class="tab-pane fade" id="to_server_' + tabID + '">To_server_ '+ tabID +' content</div>'));
    });

    var list = document.getElementById("tab-list");
});*/