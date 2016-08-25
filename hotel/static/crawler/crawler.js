var crawler = (function(){
	var url = 'www.baidu.com';
	var buttonDivName;
    var tableDivName;
    var dataTable;
    var currentIndex = 0;
    var tableDataArray = new Array();
    var urlHotelData = { "en": "http://english.ctrip.com/hotels",
                         "fr": "24",
    };
	
    function _init() {
    	if (buttonDivName==''){
    		return
    	}
    	_bindButtonDiv();
        _initTable();
    }
    function _initTable() {
        dataTable = $(tableDivName).DataTable( {
            destroy: true,
            ordering: false,
            //searching: false,
            columns: [
                { title: "Time" },
                { title: "Type" },
                { title: "Language" },
                { title: "Country" },
                { title: "PageID" },
            ],
            lengthMenu: [20, 30, 40],
        });
        
    }
    function _bindButtonDiv() {
    	$(buttonDivName).click(function(){
            _getPageIDFromBackend("http://english.ctrip.com/hotels");
    	});
    }
    function _procressData(pageid) {
        var tableRow = new Array();
        tableRow[0] = _getCurrentTime();
        tableRow[1] = "hotels";//$("#select1").val();
        tableRow[2] = "en";//$("#select2").val();
        tableRow[3] = "ccc";//$("#select3").val();
        tableRow[4] = pageid;//_getPageIDFromBackend(url);
        tableDataArray[currentIndex] = tableRow;
        currentIndex = currentIndex + 1;
        _flushDataTable();
    }
    function _flushDataTable() {
        dataTable = $(tableDivName).DataTable( {
            data: tableDataArray,
            destroy: true,
            // paging: false,
            //info: false,           
            columns: [
                { title: "Time" },
                { title: "Type" },
                { title: "Language" },
                { title: "Country" },
                { title: "PageID" },
            ],
            order: [[ 0, "desc" ]],
            //ordering: false,
            lengthMenu: [10, 20, 30, 40],
        });
    }
    function _getCurrentTime() {
        var date = new Date();
        hours = date.getHours();
        minutes = date.getMinutes();
        result = hours + ":" + minutes;
        return result
    }
    function _getPageIDFromBackend(url) {
        var pageid;
        $.get("/getpageid/" + url + "/" , function(data, status){
            //alert(JSON.stringify(data));
            //alert(data);
            _procressData(data);
        });
    }

    function setButtonDivName(divName) {
        buttonDivName = divName;
    }
    function setTableDivName(divName) {
        tableDivName = divName;
    }
    function start() {
    	_init()
        //alert(urlData['en']);
    }

	return {
		setButtonDivName: setButtonDivName,
        setTableDivName: setTableDivName,
		start: start,
	};
})();