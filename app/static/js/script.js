function loadContent(a){
    $.ajax(
        {
            type: "GET",
            url: a,
            success: function(data){
                for(i=0;i<data.length;i++){
                    var tr = document.createElement('tr');
                    for(j=0;j<data[i].length;j++){
                        var td = document.createElement('td');
                        if(j==0){
                            var a = document.createElement('a');
                            a.className = "btn btn-danger";
                            a.innerText = "Удалить";
                            a.href = data[i][j];
                            td.appendChild(a)
                            j++;
                            var b = document.createElement('a');
                            b.className = "btn btn-info";
                            b.innerText = "Изменить";
                            b.href = data[i][j];
                            td.appendChild(b)
                        }
                        else{
                            td.innerText = data[i][j];
                        }
                        tr.appendChild(td);
                    }
                    document.getElementById('table_elements').appendChild(tr)
                }
        }
    }
    );
}

function letsearch(url){
    text = document.getElementById("search").value;
    //console.log(text)
    $.ajax(
        {
            type: "GET",
            url: url,
            data: {
                'search': text
            },
            contentType: "application/json",
            success: function(data){
                var table = document.getElementById('table_elements').innerHTML = "";
                var tr = document.createElement('tr');
                for(i=0;i<data.length;i++){
                    var tr = document.createElement('tr');
                    for(j=0;j<data[i].length;j++){
                        var td = document.createElement('td');
                        td.innerText = data[i][j];
                        tr.appendChild(td);
                    }
                    document.getElementById('table_elements').appendChild(tr)
                }
            }
        }
    );
    }
