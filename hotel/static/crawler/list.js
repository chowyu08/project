var list = (function () {
	var hotelSeedButton;
    var hotelListButton;
    var hotelResultButton;
    var tableDivName;
    var resultTableDivName
    var dataTable;
    var resultTable;
    var currentIndex = 0;
    var tableData = new Array();

    var currentFileName = "";
    var listFileName = "";

	function _getFields() {
    	return {
    		"env":['online','fat8'], 
    		"site":['english','jp','fr','es','ru','de','hk','sg','my','th','id','kr'],
    		"city":['beijing','shanghai','hong-kong','sanya','guangzhou']
    	};
    }

    function _init() {
    	if (hotelSeedButton==''){
    		return
    	}
    	_initSelect();
    	_bindButtonDiv();
        _initdataTable();
    }

    function _initSelect() {
    	fields = _getFields();
    	$.each(fields, function(name, values) {
    		// console.log(name);
    		$.each(values,function (n,value) {
    			$('#'+name).append("<option value='"+value+"'>"+value+"</option>");
    		});
        });
    }

    function _initdataTable() {
        dataTable = $(tableDivName).DataTable( {
            destroy: true,
            paging: true,
            info: false,
            searching: false,
            autoWidth: false,
            columns: [
                { title: "Type" },
                { title: "URL" },
            ],
            lengthMenu: [5, 10, 20],
            columnDefs: [
                { "width": "12%", "targets": 0 }
            ]
        });
        
    }

    function _bindButtonDiv() {
    	$(hotelSeedButton).click(function(){
    		fields = _getFields();
    		var args = "";
	    	$.each(fields, function(name, values) {
	    		args = args + $('#'+name).val() + "/";
	        });
	        _getHotelSeeds(args);
            // _getHotelList(currentFileName);
            // _getHotelResult(currentFileName);
            $(hotelSeedButton).attr('disabled',"true")
    	});
        $(hotelListButton).click(function(){
            _getHotelList(currentFileName);
            $(hotelListButton).attr('disabled',"true");
        });
        $(hotelResultButton).click(function(){
            _getHotelResult(currentFileName);
            // $(hotelResultButton).attr('disabled',"true");
        });
    }

    function _procressSeedsData(newdata) {
        // var table = new Array();
        fulllfilename = newdata['filename'];//_getPageIDFromBackend(url);
        // console.log(hotelList)
        filename = fulllfilename.substring(fulllfilename.lastIndexOf('/')+1);
        currentFileName = filename;
        tableRow = new Array();
        if(fulllfilename!='false'){
            tableRow[0] = "Seed";
            tableRow[1] ="<a href=/hotel/download/seed/"+ filename + "><i class='fa fa-user fa-fw'></i>" + filename +"</a>";
            tableData[currentIndex] = tableRow;
            currentIndex = currentIndex + 1;
        }else{
            tableData[currentIndex] = ['error','ERROR']
        }
        _flushTable();
    }

    function _procressListData(newdata) {
        filename = newdata['filename'];
        currentFileName = filename;
        tableRow = new Array();
        if(fulllfilename!='false'){
            tableRow[0] = "List";
            tableRow[1] ="<a href=/hotel/download/list/"+ filename + "><i class='fa fa-user fa-fw'></i>" + filename +"</a>";
            tableData[currentIndex] = tableRow;
            currentIndex = currentIndex + 1;
        }else{
            tableData[currentIndex] = ['error','ERROR']
        }
        _flushTable();
    }
    function _procressResultData(newdata) {
        filename = newdata['filename'];
        // currentFileName = filename;
        tableRow = new Array();
        if(fulllfilename!='false'){
            tableRow[0] = "Type";
            tableRow[1] ="<a href=/hotel/download/type/"+ filename + "><i class='fa fa-user fa-fw'></i>" + filename +"</a>";
            tableData[currentIndex] = tableRow;
            currentIndex = currentIndex + 1;
        }else{
            tableData[currentIndex] = ['error','ERROR']
        }
        _flushTable();
    }
    function _flushTable() {
        dataTable.rows().remove().draw( true );
        $.each(tableData,function(n, value) {
            // console.log(value);
            dataTable.row.add(value);
        })
        dataTable.draw(true);
    }

    function _getHotelSeeds(inputArgs) {
    	// console.log("/gethotellist/"+ inputArgs);
        $.get("/hotel/getSeeds/"+ inputArgs, function(data, status){
            _procressSeedsData(data);
        });
    }
    function _getHotelList(inputArgs) {
        $.get("/hotel/getList/"+ inputArgs, function(data, status){
             // alert(JSON.stringify(data));
            // alert(data['filename'])
            _procressListData(data);
        });
    }
    function _getHotelResult(inputArgs) {
        $.get("/hotel/getType/"+ inputArgs, function(data, status){
             // alert(JSON.stringify(data));
            // alert(data['filename'])
            _procressResultData(data);
        });
    }

    function setHotelSeedButtonDivName(divName) {
        hotelSeedButton = divName;
    }
    function setHotelListButtonDivName(divName) {
        hotelListButton = divName;
    }
    function setHotelResultButtonDivName(divName) {
        hotelResultButton = divName;
    }
    function setTableDivName(divName) {
        tableDivName = divName;
    }

    function start() {
    	_init()
    }

	return {
		setHotelSeedButtonDivName: setHotelSeedButtonDivName,
        setHotelResultButtonDivName: setHotelResultButtonDivName,
        setHotelListButtonDivName: setHotelListButtonDivName,
        setTableDivName: setTableDivName,
		start: start,
	};
})();