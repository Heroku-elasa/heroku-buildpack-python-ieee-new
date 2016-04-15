var casper = require('casper').create();

casper.start('http://www.sciencedirect.com/science/article/pii/S0142061514004463', function() {
    this.echo(this.getTitle());
});

casper.thenOpen('http://phantomjs.org', function() {
    this.echo(this.getTitle());
});

casper.run();

//casperjs casper-sample.js --proxy=143.89.225.246:3128