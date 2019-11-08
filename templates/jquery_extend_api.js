jQuery["postJSON"] = function(url, data, callback) {
    // shift arguments if data argument was omitted
    if (jQuery.isFunction(data)) {
        callback = data;
        data = undefined;
    }

    return jQuery.ajax({
        url: url,
        type: "POST",
        contentType: "application/json; charset=utf-8",
        crossDomain: true,
        headers: {
            'Access-Control-Allow-Origin': '*'
        },
        dataType: "json",
        data: data,
        success: callback
    });
};

jQuery["getJSON"] = function(url, callback) {
    return jQuery.ajax({
        url: url,
        type: "GET",
        contentType: "application/json; charset=utf-8",
        crossDomain: true,
        headers: {
            'Access-Control-Allow-Origin': '*'
        },
        dataType: "json",
        success: callback
    });
};