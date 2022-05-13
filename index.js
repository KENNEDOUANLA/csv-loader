$(function() {

    $('input[name="file_csv"]').on('change', function(e) {
        let file_csv = $('input[name="file_csv"]').prop('files')
        const reader = new FileReader();
        e.preventDefault();
        reader.onload = function(e) {
            const csvTable = csvToArray(e.target.result)
        };

        reader.readAsText(file_csv[0]);
    })


    function csvToArray(str, delimiter = ",") {
        let headers = str.slice(0, str.indexOf("\n"));
        headers = headers.slice(0, str.indexOf("\r")).split(delimiter);
        const rows = str.slice(str.indexOf("\n") + 1).split("\n");
        let arr = [];
        rows.forEach(element => {
            const data = element.split('"');
            // verifier si la donnnées contient un ",".("COMMUNE,SAMSON")
            // s'il y a aucun caractere, element n'aura n'aura pas de double cote
            if (data.length === 1) {
                const values = data[0].split(delimiter);
                arr.push(headers.reduce(function(Data, header, index) {
                    Data[header] = values[index];
                    return Data;
                }, {}));
            } else {
                const size = data.length - 1
                const Data = {};
                Data[headers[0]] = data[0] = data[0].slice(0, -1);
                Data[headers[1]] = data[1];
                Data[headers[headers.length - 1]] = data[size] = data[size].slice(1, );

                let index = 2;
                while (index < size) {
                    if (index % 2 == 0) {
                        Data[headers[index]] = data[index] = data[index].slice(0, -1).slice(1, );
                    } else {
                        Data[headers[index]] = data[index]
                    }
                    index++;
                }
                arr.push(Data)
            }
        });
        return arr;
    }

})