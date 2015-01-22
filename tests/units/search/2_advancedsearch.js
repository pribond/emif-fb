module.exports = {
  "Searching using Advanced Search" : function (browser) {
    browser
      .login(browser.globals.username, browser.globals.password)
      .waitForElementVisible('#actions a[href="advancedSearch/49/1"]', 10000, 'Dashboards opens and link is visible')
      .click('#actions a[href="advancedSearch/49/1"]')
      .waitForElementVisible('li[id="li_qs_1"]', 10000, 'Advanced search loads with success')
      .waitForElementVisible('input[id="question_1.01"]', 10000, 'Questionset 1 Loaded with success')
      .clearValue('input[id="question_1.01"]')
      .setValue('input[id="question_1.01"]', 'ARS')
      .click('button[type=submit]')
      .waitForElementVisible('a[data-acronym="ARS"]', 10000, 'Search Returned with success')
      .end();
  }
};