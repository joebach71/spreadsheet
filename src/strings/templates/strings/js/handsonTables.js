var $$ = function(id) {
  return document.getElementById(id);
},
title = $$('title'),
// handson tables
confirmHandsonTable = $$('confirmHandsonTable'),
badHtmlHandsonTable = $$('badHtmlHandsonTable'),
savedHandsonTable = $$('savedHandsonTable'),
notSavedHandsonTable = $$('notSavedHandsonTable'),
// panels
mainPanel = $$('mainPanel'),
confirmPanel = $$('confirmPanel'),
badHtmlPanel = $$('badHtmlPanel'),
savedPanel = $$('savedPanel'),
notSavedPanel = $$('notSavedPanel'),
productId = $$('productId'),
save = $$('save'),
confirm = $$('confirm'),
cancel = $$('cancel'),
days = $$('days'),
language = $$('language');

$('input:file').change(function(){
  if ($(this).val()) {
    $('button:submit').attr('disabled',false); 
  } 
});

hotSavedTable = new Handsontable(savedHandsonTable, {
  colHeaders: ['ID', 'Language', 'Before', 'After'],
  rowHeaders: true,
  manualColumnResize: [300, 100, 300, 300],
  manualRowResize: true,
  fixedColumnsLeft: 1,
  stretchH: 'last',
  preventOverflow: 'horizontal',
  currentRowClassName: 'currentRow',
  columns: [
    {
      data: 0,
      readOnly: true,
    },
    {
      data: 1,
      readOnly: true,
    },
    {
      data: 2,
      readOnly: true,
      renderer: plainRenderer
    },
    {
      data: 3,
      readOnly: true,
      renderer: plainRenderer
    },
  ]
});

hotNotSavedTable = new Handsontable(notSavedHandsonTable, {
  colHeaders: ['ID', 'Language', 'Before', 'After', 'Errors'],
  rowHeaders: true,
  manualColumnResize: [300, 100, 200, 200, 200],
  manualRowResize: true,
  stretchH: 'last',
  preventOverflow: 'horizontal',
  fixedColumnsLeft: 1,
  currentRowClassName: 'currentRow',
  columns: [
    {
      data: 0,
      readOnly: true,
    },
    {
      data: 1,
      readOnly: true,
    },
    {
      data: 2,
      readOnly: true,
      renderer: plainRenderer
    },
    {
      data: 3,
      readOnly: true,
      renderer: plainRenderer
    },
    {
      data: 4,
      readOnly: true,
      renderer: plainRenderer
    },
  ]
});

hotBadHtml = new Handsontable(badHtmlHandsonTable, {
  colHeaders: ['ID', 'Language', 'Before', 'After', 'Reason'],
  rowHeaders: true,
  manualColumnResize: [300, 100, 200, 200, 200],
  manualRowResize: true,
  fixedColumnsLeft: 1,
  stretchH: 'last',
  preventOverflow: 'horizontal',
  currentRowClassName: 'currentRow',
  columns: [
    {
      data: 'stringid',
      readOnly: true,
    },
    {
      data: 'field',
      readOnly: true,
    },
    {
      data: 'before',
      readOnly: true,
      renderer: plainRenderer
    },
    {
      data: 'after',
      readOnly: true,
      renderer: plainRenderer
    },
    {
      data: 'reason',
      readOnly: true,
      renderer: plainRenderer
    }
  ]
});

hotConfirm = new Handsontable(confirmHandsonTable, {
  colHeaders: ['ID', 'Language', 'Before', 'After'],
  rowHeaders: true,
  manualColumnResize: true,
  manualRowResize: true,
  fixedColumnsLeft: 1,
  preventOverflow: 'horizontal',
  stretchH: 'last',
  currentRowClassName: 'currentRow',
  columns: [
    {
      data: 'stringid',
      readOnly: true,
    },
    {
      data: 'field',
      readOnly: true,
    },
    {
      data: 'before',
      readOnly: true,
    },
    {
      data: 'after',
    },
  ],
  afterChange: function (change, source) {
    if (source === 'loadData') {
    return; //don't save this change
    }
    if (change != null) {
      var instance = this;
      // if there are multiple changes, then I must get all its stringids
      
      $(change).each(function () {
        // changed data [row, col, before, after]
        var changedData = this;
        // change the color of edited cell
        var cell = instance.getCell(changedData[0], instance.propToCol(changedData[1]));
        if (cell) {
          cell.style.color = 'red';
        }
        
        // replace the row with stringid
        var stringid = instance.getDataAtCell(changedData[0], 0);
        // this[0] = stringid;
        if (changedData[2] === changedData[3]) {
          return; // don't do anything is no change
        }
        if (data[stringid+'.'+changedData[1]]) {
          changedData[2] = data[stringid+'.'+changedData[1]]['before'];
        }
        // change the color of cell???
        data[stringid+'.'+changedData[1]] = {'stringid': stringid, 'field': changedData[1], 'before': changedData[2], 'after': changedData[3] };
      });
    }
  }
});

{% for product in products %}
tempData["{{ product.category }}"] = {};
hTables["{{ product.category }}"] = new Handsontable($$('handsonTable_'+ "{{ product.category }}"), {
  colHeaders: colHeaders,
  hiddenColumns: {
    columns: hiddenColumns,
    indicators: false,
    copyPasteEnabled: false
  },
  rowHeaders: true,
  contextMenu: ['undo'],
  manualColumnResize: [300, 100, 100, 300, 300{% for name in publishers %}, 300{% endfor %}], 
  manualRowResize: true,
  fixedColumnsLeft: 1,
  height: 600,
  preventOverflow: 'both',
  currentRowClassName: 'currentRow',
  columnSorting: true,
  beforeColumnSort: function (col, order) {
    sortTable('{{ product.category }}', col, order, function() {
      return false;
    });
  },
  sortIndicator: true,
  cells: function (row, col, prop) {
    var cellProperties = {};
    if (col > 2) {
      cellProperties.renderer = "customCellRenderer";
    }
    return cellProperties;
  },
  columns: [
    {
      data: 'stringid',
      readOnly: true,
    },
    {
      data: 'description1',
      {% if not editDesc %}readOnly: true{% endif %}
    },
    {
      data: 'description2',
      {% if not editDesc %}readOnly: true{% endif %}
    },
    {
      data: 'Korea',
      {% if not editKorea %}readOnly: true{% endif %}
    },
    {
      data: 'Korea_modified_at'
    },
    {
      data: 'English',
      {% if not editEnglish %}readOnly: true{% endif %}
    },
    {
      data: 'English_modified_at'
    }
    {% for name in publishers %}
    ,{
      data: '{{ name }}',
    },
    {
      data: '{{ name }}_modified_at'
    }
    {% endfor %}
  ],
  afterChange: function (change, source) {
    if (source === 'loadData') {
      return; //don't save this change
    }
    if (change !== null) {
      var instance = this;
      $(change).each(function () {
        // change the color of edited cell
        // changedData = [row, col, before, after]
        var changedData = this;
        if (changedData[2] === changedData[3]) {
          return; // don't do anything is no change
        }
        var cell = instance.getCell(changedData[0], instance.propToCol(changedData[1]));
        if (cell) {
          cell.style.color = '#0000FF';
        }
        // replace the row with stringid
        var stringid = instance.getDataAtCell(changedData[0], 0);
        if (tempData["{{ product.category }}"][stringid+'.'+changedData[1]]) {
          changedData[2] = tempData["{{ product.category }}"][stringid+'.'+changedData[1]]['before'];
        }
        // should change the color of cell???
        tempData["{{ product.category }}"][stringid+'.'+changedData[1]] = { 'stringid': stringid, 'field': changedData[1], 'before': changedData[2], 'after': changedData[3] };
      });
    }
  }
});
{% endfor %}
