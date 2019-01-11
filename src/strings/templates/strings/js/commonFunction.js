{% load strings_extras %}

var xhr;
var active=false;
var hTables = {};
var tempData = {};
var title;
var confirmHandsonTable;
var badHtmlHandsonTable;
var savedHandsonTable;
var mainPanel;
var confirmPanel;
var badHtmlPanel;
var savedPanel;
var notSavedPanel;
var productId;
var save;
var confirm;
var cancel;
var days;
var language;
var hotConfirm;

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
function confirm() {
  // save all cell's data
  var tablename = $("#tablename").val();
  var url = '/localtext/products/'+$("#productId").val()+'/confirm';
  $.ajax({
    url,
    type: 'POST',
    data: JSON.stringify(hotConfirm.getData()),
    "beforeSend": function(xhr, settings) {
      $.ajaxSettings.beforeSend(xhr, settings);
    },
    success: function (results) {
      showTab(document.getElementById('tab-review'));
      // update page loads
      hotSavedTable.loadData(results.saved);
      hotNotSavedTable.loadData(results.notSaved);
    },
    error: function(error) {
      alert("Error: " + error.statusText);
      error.preventDefault();
    }
  });

}
function save(elem, pk, product, category) {
  var data = JSON.stringify(tempData[category]);
  $.ajax({
    url : '/localtext/products/'+pk+'/save/',
    type: 'POST',
    data,
    dataType: 'json',
    beforeSend: function(xhr, settings) {
      $.ajaxSettings.beforeSend(xhr, settings);
    },
    success: function (results) {
      var tab = document.getElementById('tab-saving');
      showTab(tab);
      hotConfirm.loadData(results.data);
      if (!results.data.length) {
        $("#confirm").hide();
      }
      // 4. errors
      hotBadHtml.loadData(results.error);
      $("#productId").val(results.product);
      $("#tablename").val(category);
    },
    error: function(e) {
      alert("Error: " + e.statusText);
    },
  });
  event.preventDefault();
}
var gotoPage = (identifier, page) => {
  var app_name = $("#app_name").val();
  var params = getConditions(identifier);
  params.page = page;
  var data = {
    url: `/api/${app_name}_${identifier}/`,
    params,
    identifier
  }
  loadLocalText(data); 
}
var setPage = function(id, current, total) {
  var pageSelect = $("#goToPage_"+id);
  let options = "";
  for (i = 1; i <= parseInt(total); i++) {
      if (i === parseInt(current)) {
          options += '<option value="'+i+'" selected>'+i+'</option>';
      } else {
          options += '<option value="'+i+'">'+i+'</option>';
      }
  }
  pageSelect.children().remove();
  pageSelect.append(options);
}
var setPageMenus = function(args) {
  var { identifier, total, next, previous, page, page_size } = args;
  var from = ( page - 1) * page_size + 1;
  var to = page * page_size;
  $("#perPage_"+identifier).val(page_size);
  if (next == null) {
    $('#next_'+identifier).prop("disabled", true);
    to = total % page_size + ( page - 1) * page_size;
  } else {
    $('#next_'+identifier).prop("disabled", false); 
  }
  if (previous == null) {
    $('#previous_'+identifier).prop("disabled", true);
  } else {
    $('#previous_'+identifier).prop("disabled", false); 
  }
  $("#page_count_"+identifier).text(` ${ from } - ${ to }`);
  $("#total_count_"+identifier).text(` of ${total} ${identifier.toLowerCase()}`);
  var total_pages = parseInt(total / page_size, 10) + (total % page_size? 1 : 0);
  $("#total_page_"+identifier).text(` of ${total_pages} `);

  setPage(identifier, page, total_pages);
}
var attributes = [{% for name in publishers %}, '{{ name }}'{% endfor %}];
if ({% if editEnglish %}true{% else %}false{% endif %}) {
  attributes.push('English');
}
if ({% if editKorea %}true{% else %}false{% endif %}) {
  attributes.push('Korea');
}
var convert2object = function(data) {
  /* convert value into object property */
  data.forEach(function(row) {
    attributes.forEach(function(name) {
      if (row[name]) {
        row[name] = { text: row[name], update_require: row[`${name}_require_update`] || false }
      }
    })
  }, this);
  return data;
}

function loadLocalText(data, callback) {
  if (active) { console.log("killing active"); xhr.abort(); }
  active = true;
  xhr = $.ajax({
    dataType: "json",
    url: data.url,
    data: data.params,
    success: function(result, statusText, xhr) {
      if (result != null) {
        hTables[data.identifier].loadData(result.results);
        hTables[data.identifier].updateSettings({
          cells: function (row, col, prop) {
            var cellProperties = {};
            if (col > 2) {
              cellProperties.renderer = "customCellRenderer";
            }
            return cellProperties;
          },
        });
        var args = {
          total: result.count,
          page_size: data.params.page_size,
          next: result.next,
          previous: result.previous,
          page: data.params.page || 1,
          identifier: data.identifier
        };
        setPageMenus(args);
      }
    },
    error: function(xhr, status, errorMsg) {
      console.info("ERROR: ", status, ", msg: ", errorMsg);
    },
    complete: function() {
      active = false;
      callback && callback();
    }
  });
}

function showDataTable(elem, pk, product, tablename) {
  // upload clicked data
  $(productId).val(pk);
  var params = getConditions(tablename);
  var data = {
    url: `/api/${product}_${tablename}/`,
    params,
    identifier : tablename
  }
  loadLocalText(data, function(result) {
    var input = $('input#filterValue_'+tablename);
    if ($('#filter_'+tablename).val() === "") {
      input.val('');
      input.prop('disabled', true);
    } else {
      input.prop('disabled', false);
    }
  });
  // change tabsX into tabs-X in order to find the correct tab content
  var tabContentIdToShow = elem.id.replace(/Link-/g, 'tab_');
  var tab = document.getElementById(tabContentIdToShow);
  showTab(tab);
}

function showTab(element) {
  hideTab();
  if (element) {
    element.style.display = 'block';
  }
}
  
function hideTab()  {
  $.each($(".fade"), function(index, tab) { 
    tab.style.display = 'none';
  });
  // if (document.getElementById('tab-saveing').style.display == 'block') {
  document.getElementById('tab-saving').style.display = 'none';
  // }
  // if (document.getElementById('review').style.display == 'block') {
  document.getElementById('tab-review').style.display = 'none';
  // }
}
function getConditions(identifier) {
  var inputs = {
    format: 'json',
  };
  // entries
  if ($("#perPage_"+identifier).val()) {
    inputs['page_size'] = $("#perPage_"+identifier).val() || 250;
  }
  // page
  inputs['page'] = parseInt($("#goToPage_"+identifier).val() || 1, 10);
  // search
  if ($("#filterValue_"+identifier).val() && $("#filter_"+identifier).val()) {
    inputs[$("#filter_"+identifier).val() + '__icontains'] = $("#filterValue_"+identifier).val();
  }
  // status
  if ($('input[name=status_'+identifier+']:checked').val() === 'untranslated' || $('input[name=status_'+identifier+']:checked').val() === 'unmodified') {
    inputs[$('input[name=status_'+identifier+']:checked').val()] = true;
  }
  if ($('#ordering_'+identifier).val()) {
    inputs['ordering'] = $('ordering_'+identifier).val();
  }
  return inputs;
}

function upload_submit(id) {
  var self = $(this);
  document.getElementById(id).submit();
}
function editedCellRenderer(instance, td, row, col, prop, value, cellProperties) {
  Handsontable.renderers.TextRenderer.apply(this, arguments);
  td.style.color = 'red';
};
Handsontable.renderers.registerRenderer('editedCellRenderer', editedCellRenderer);
function customCellRenderer(instance, td, row, col, prop, value, cellProperties) {
  Handsontable.renderers.TextRenderer.apply(this, arguments);
  if (col === 5 && {% if editEnglish %}false{% else %}true{%endif %}) {
    return;
  }
  if (!value || value === '') {
    td.style.background = '#EEEEEE';
    return;
  }
  if (col > 4 && !hiddenColumns.includes(col) && new Date(instance.getDataAtCell(row, col + 1)) <= new Date(instance.getDataAtCell(row, 4)) ) {
    td.style.background = '#FF0000';
  }
};
Handsontable.renderers.registerRenderer('customCellRenderer', customCellRenderer);
function plainRenderer(instance, td, row, col, prop, value, cellProperties) {
  Handsontable.renderers.TextRenderer.apply(this, arguments);
  td.className = 'plain';
};
Handsontable.renderers.registerRenderer('plainRenderer', plainRenderer);

function encodeQueryData(data) {
  var ret = [];
  for (let d in data)
    ret.push(encodeURIComponent(d) + '=' + encodeURIComponent(data[d]));
  return ret.join('&');
}
var sortByHeaders = ['stringid', 'description1', 'description2', 'Korea', 'Korea_modified_at', 'English', 'English_modified_at'{% for name in publishers %}, '{{ name }}', '{{ name }}_modified_at'{% endfor %}];
var sortTable = function(identifier, col, order, callback) {
  var sortBy = sortByHeaders[col] + '_modified_at';
  var ascending = '';
  if (!order) {
    ascending = '-';
  }
  var params = getConditions(identifier);
  params['ordering']= `${ascending}${sortBy}`;
  const app_name = $("#app_name").val();
  const data = {
    url: `/api/${app_name}_${identifier}/`,
    params,
    identifier
  };
  loadLocalText(data, function() {
    callback && callback(data);
  });
};

var colHeaders = ['id', 'description1', 'description2', 'kor', 'Korea_modified_at', 'eng', 'English_modified_at'{% for name in publishers %}, '{{ name | lower | firstThree }}', '{{ name }}_modified_at'{% endfor %}];
var hiddenColumns = [4, 6, 8, 10, 12, 14];

{% for product in products %}
$("#search_{{ product.category }}").on('click', function() {
  var params = getConditions("{{ product.category }}");
  var data = {
    url: '/api/{{ product.name }}_{{ product.category }}/',
    params,
    identifier : "{{ product.category }}"
  }
  loadLocalText(data);
});
$("#filter_{{ product.category }}").on('change', function() {
  var filter = $(this).val();
  var input = $('input#filterValue_{{ product.category }}');
  if (filter === "") {
    input.val('');
    input.prop('disabled', true);
  } else {
    input.prop('disabled', false);
  }
});
// untranslated, unmodified filtering
$("input[name='status_{{ product.category }}']").on('click', function() {
  // get translated only
  var params = getConditions("{{ product.category }}");
  var data = {
    url: '/api/{{ product.name }}_{{ product.category }}/',
    params : params,
    identifier : "{{ product.category }}"
  }
  loadLocalText(data);
});
$('#next_{{ product.category }}').click( function() {
  const params = getConditions("{{ product.category }}");
  params.page = params.page + 1;
  const data = {
    url: "/api/{{ product.name }}_{{ product.category }}",
    params,
    identifier : "{{ product.category }}"
  }
  loadLocalText(data);

});
$('#previous_{{ product.category }}').click(function() {
  var params = getConditions("{{ product.category }}");
  params.page = params.page - 1;
  var data = {
    url: "/api/{{ product.name }}_{{ product.category }}",
    params,
    identifier : "{{ product.category }}"
  }
  loadLocalText(data);
});
// Change Per Page Count
$('#perPage_{{ product.category }}').change( function () {
  var params = getConditions("{{ product.category }}");
  params["page"] = 1;
  var data = {
    url: '/api/{{ product.name }}_{{ product.category }}/',
    params,
    identifier : "{{ product.category }}"
  }
  loadLocalText(data);
});
$('#goToPage_{{ product.category }}').change( function() {
  var self = $(this);
  var params = getConditions("{{ product.category }}");
  params.page = parseInt(self.val(), 10);
  var data = {
    url: "/api/{{ product.name }}_{{ product.category }}",
    params,
    identifier : "{{ product.category }}"
  }
  loadLocalText(data);
});
$('#export_xlsx_{{ product.category }}').on('click', () => {
  var params = {};
  if ($("#filterValue_{{ product.category }}").val()) {
    params['filter'] = $("#filter_{{ product.category }}").val();
  }
  if ($("#filterValue_{{ product.category }}").val()) {
    params['pattern'] = $("#filterValue_{{ product.category }}").val(); 
  }
  // only untranslated
  if ($('#untranslated_{{ product.category }}').is(":checked")) {
    params['untranslated'] = $('#untranslated_{{ product.category }}').is(":checked");
  }
  if ($('#unmodified_{{ product.category }}').is(":checked")) {
    params['unmodified'] = $('#unmodified_{{ product.category }}').is(":checked");
  }
  xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    var a;
    if (xhttp.readyState === 4 && xhttp.status === 200) {
      a = document.createElement('a');
      a.href = window.URL.createObjectURL(xhttp.response);
      a.download = '{{ product.category }}.xlsx';
      a.style.display = 'none';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }
  };
  var querystring = encodeQueryData(params);
  var url = "/localtext/products/{{ product.pk }}/export?"+querystring;
  xhttp.open("GET", url, true);
  xhttp.setRequestHeader("Content-Type", "application/json");
  xhttp.responseType = 'blob';
  xhttp.send();
});

{% endfor %}
