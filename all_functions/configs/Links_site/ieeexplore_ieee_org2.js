var page = new WebPage()
, output = { errors: [], results: null };
if (phantom.args.length == 0) {
    console.log('You must specify a city, eg. "Paris, France"');
    phantom.exit(1);
}
page.open('http://www.google.fr/search?q=meteo+' + phantom.args[0], function (status) {
    if (status !== 'success') {
        output.errors.push('Unable to access network');
    } else {
        var cells = page.evaluate(function(){
            try {
                var cells = document.querySelectorAll('.tpo tr tr')[4].querySelectorAll('td');
                return Array.prototype.map.call(cells, function(cell) {
                    return cell.innerText.replace(/[^0-9]/g, '');
                });
            } catch (e) {
                return [];
            }
        });
        if (!cells || !cells.length > 0) {
            output.errors.push('No valid meteo data found');
        } else {
            output.results = {
                city: phantom.args[0],
                today: {
                    afternoon: cells[1],
                    morning:   cells[2],
                },
                tomorrow: {
                    afternoon: cells[3],
                    morning:   cells[4],
                }
            };
        }
        console.log(JSON.stringify(output, null, '    '));
    }
    phantom.exit();
});