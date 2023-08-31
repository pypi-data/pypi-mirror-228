var addFiltersToDynamicListingApp = function () {
  var dateRangeFilters, removeFilterButtons


  function submit(form) {
    var data = Array.from(new FormData(form))
        .filter(function ([k, v]) {
          return v
        }),
      params = new URLSearchParams(data)

    location.href = location.origin + location.pathname + "?" + params.toString()
  }

  function initDateRangeFilters() {
    $('[data-date-range-filter="true"]').daterangepicker({}, function (start, end) {
      var $from = this.element.siblings(`[data-range-from="${this.element.data('name')}"]`),
        $to = this.element.siblings(`[data-range-to="${this.element.data('name')}"]`)

      $from.val(start.format('MM/DD/YYYY'))
      $to.val(end.format('MM/DD/YYYY'))
      submit(this.element.closest('form')[0])
    })
  }

  function initFilterForms() {
    initDateRangeFilters()

    $(document)
      .on('change', '[data-instant-filter="true"]', function (e) {
        submit($(this).closest('form')[0])
      })
      .on('submit', '[data-toggle="filters"]', function (e) {
        e.preventDefault()
        submit(this)
      })
      .on('click', '[data-reset-filters="true"]', function (e) {
        e.preventDefault()
        location.href = location.origin + location.pathname
      })
      .on('search', 'input[type="search"]', function (e) {
        submit($(this).closest('form')[0])
      })

    removeFilterButtons.forEach(function (button) {
      button.addEventListener('click', function (e) {
        /* e.preventDefault()
         var params = new URLSearchParams(location.search),
           keyToRemove = button.getAttribute('data-key'),
           valueToRemove = button.getAttribute('data-value'),
           values = params.getAll(keyToRemove),
           updatedValues = values.filter(function (value) {
             return value !== valueToRemove
           })

         params.delete(keyToRemove)
         updatedValues.forEach(function (value) {
           params.append(keyToRemove, value)
         })

         var newQueryString = params.toString()
         console.log(newQueryString)
         location.href = location.origin + location.pathname + (newQueryString ? "?" + newQueryString : "")*/
        e.preventDefault();

        var params = new URLSearchParams(location.search);
        var keysToRemove = button.getAttribute('data-key').split(','); // Split the comma-separated keys
        var valuesToRemove = button.getAttribute('data-value').split(','); // Split the comma-separated values

        keysToRemove.forEach(function (keyToRemove, index) {
          var valueToRemove = valuesToRemove[index];

          var currentValues = params.getAll(keyToRemove);
          var updatedValues = currentValues.filter(function (value) {
            return value !== valueToRemove;
          });

          params.delete(keyToRemove);

          updatedValues.forEach(function (value) {
            params.append(keyToRemove, value);
          });
        });

        var newQueryString = params.toString();
        location.href = location.origin + location.pathname + (newQueryString ? "?" + newQueryString : "");
      })
    })
  }


  return {
    init() {
      dateRangeFilters = $('[data-date-range-filter="true"]')
      removeFilterButtons = document.querySelectorAll('[data-filter-remove="true"]')
      initFilterForms()
    }
  }
}()

var RowSelection = function () {
  var masterCheckbox, checkboxes, bulkActions, selectedCount, rightFilters, selectedItemsInput

  function updateSelectedItemsInput() {
    const selectedCheckboxes = document.querySelectorAll('[data-selection-checkbox="item"]:checked');
    const selectedValues = Array.from(selectedCheckboxes).map(checkbox => checkbox.value);
    selectedItemsInput.forEach(function (input) {
      input.value = selectedValues.join(",");
    })
  }

  function updateActionsContainer() {
    const selectedCheckboxes = document.querySelectorAll('[data-selection-checkbox="item"]:checked'),
      count = selectedCheckboxes.length


    selectedCount.textContent = `Selected items: ${count}`
    if (count > 0) {
      bulkActions.classList.remove("d-none")
      rightFilters.classList.add("d-none")
    } else {
      bulkActions.classList.add("d-none")
      rightFilters.classList.remove("d-none")
    }
  }

  function initialize() {
    if (masterCheckbox) {
      masterCheckbox.addEventListener("change", function () {
        const isChecked = masterCheckbox.checked

        checkboxes.forEach(function (checkbox) {
          checkbox.checked = isChecked
        })
        updateActionsContainer()
        updateSelectedItemsInput()
      })
    }

    checkboxes.forEach(function (checkbox) {
      checkbox.addEventListener("change", function () {
        if (masterCheckbox)
          masterCheckbox.checked = [...checkboxes].every(checkbox => checkbox.checked)
        updateActionsContainer()
        updateSelectedItemsInput()
      })
    })

    updateActionsContainer()
    updateSelectedItemsInput()
  }

  return {
    init() {
      masterCheckbox = document.querySelector('[data-selection-checkbox="master"]')
      checkboxes = document.querySelectorAll('[data-selection-checkbox="item"]')
      bulkActions = document.querySelector('[data-bulk-actions="true"]')
      selectedCount = document.querySelector('[data-selected-count="true"]')
      rightFilters = document.querySelector('[data-right-filters="true"]')
      selectedItemsInput = document.querySelectorAll('[data-selected-items="true"]')
      if (masterCheckbox || checkboxes.length)
        initialize()
    }
  }
}()

var BulkActions = function () {
  var actionsButtons, selectedItems, FromEl

  function sendRequest({method, url, forceReload, callback, inputType}) {
    const headers = new Headers({
      "X-CSRFToken": csrfToken,
      'Content-Type': 'application/json',
    });

    fetch(url, {
      method: method,
      headers: headers,
      body: JSON.stringify(getValue(inputType))
    })
      .then(response => {
        if (!response.ok) {
          return response.json()
            .then(function (errorData) {
              throw new Error(errorData.message);
            })
        }
        return response.json();
      })
      .then(res => {
        toastr.success(res['message']);
        if (forceReload) {
          location.reload();
        } else if (callback && !forceReload) {
          let cb = window;
          const callbackSplit = callback.split('.');
          for (const obj of callbackSplit) {
            cb = cb[obj];
          }
          if (typeof cb === 'function') {
            cb.call(res);
          }
        }
      })
      .catch(error => {
        toastr.error(error.message);
        console.error(error.message);
      });
  }

  function hasAttr(el, attr) {
    return el.hasAttribute(attr)
  }

  function getAttr(el, attr, initial = null) {
    if (hasAttr(el, attr)) {
      return el.getAttribute(attr)
    }
    return initial
  }

  function getValue(inputType) {
    var value = {type: inputType}
    switch (inputType) {
      case 'selected':
        value['value'] = selectedItems.value
        break
      case 'queryset':
        var queryString = window.location.search,
          params = new URLSearchParams(queryString)
        value['value'] = params.toString()
        break
      case "none":
        value['value'] = null
    }
    return value
  }

  function initOptions(button) {
    var options = {},
      asForm = getAttr(button, 'data-as-form', false) === 'true',
      method = getAttr(button, 'data-request-method', 'GET'),
      url = button.getAttribute('href'),
      inputType = getAttr(button, 'data-input-type', 'selected')
    options.id = Date.now()
    options.message = getAttr(button, 'data-confirm-message', gettext('Are you sure you would like to do this action!'))

    if (asForm) {
      var values = getValue(inputType),
        inputs = []
      for (var key in values) {
        if (values.hasOwnProperty(key)) {
          inputs.push(`<input type="hidden" name="${key}" value="${values[key]}">`)
        }
      }
      options.html = `<form action="${url}" method="${method}" id="bulk-action-form-${options.id}">
        <h2>${options.message}</h2>
        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
        ${inputs.join('')}
      </form>`
    }
    options.icon = getAttr(button, 'data-confirm-icon', 'warning')
    options.yes = getAttr(button, 'data-confirm-yes', gettext('Yes, do it!'))
    options.no = getAttr(button, 'data-confirm-no', gettext('No, cancel!'))
    options.cancel = {
      text: getAttr(button, 'data-cancel-message', gettext("Your action has been cancelled!.")),
      icon: getAttr(button, 'data-cancel-icon', 'error'),
      button: getAttr(button, 'data-cancel-action', gettext("Ok, got it!")),
    }
    options.requestParams = {
      method,
      url,
      forceReload: getAttr(button, 'data-force-reload', true) !== 'false',
      callback: getAttr(button, 'data-callback', false),
      inputType,
      asForm
    }
    return options
  }

  function fireConfirmMessage(options) {
    var alertOptions = {
      text: options.message,
      icon: options.icon,
      buttonsStyling: false,
      showCancelButton: true,
      confirmButtonText: options.yes,
      cancelButtonText: options.no,
      customClass: {
        confirmButton: "btn btn-primary",
        cancelButton: "btn btn-secondary",
      }
    }
    if (options.requestParams.asForm)
      alertOptions.html = options.html

    Swal.fire(alertOptions).then(function (result) {
      if (result.value) {
        if (!options.requestParams.asForm)
          sendRequest(options.requestParams)
        else
          document.getElementById(`bulk-action-form-${options.id}`).submit()
      } else if (result.dismiss === 'cancel') {
        Swal.fire({
          text: options.cancel.text,
          icon: options.cancel.icon,
          buttonsStyling: false,
          confirmButtonText: options.cancel.button,
          customClass: {
            confirmButton: "btn btn-primary",
          }
        });
      }
    });
  }

  function initHandlers() {
    actionsButtons.forEach(function (button) {
      button.addEventListener('click', function (e) {
        e.preventDefault()
        fireConfirmMessage(initOptions(button))
      })
    })
  }

  return {
    init() {
      actionsButtons = document.querySelectorAll('[data-toggle="bulk-action"]')
      selectedItems = document.querySelector('[data-selected-items="true"]')
      initHandlers()
    }
  }
}()


if (document.readyState !== 'loading' && document.body) {
  addFiltersToDynamicListingApp.init()
  RowSelection.init()
  BulkActions.init();
} else {
  document.addEventListener('DOMContentLoaded', addFiltersToDynamicListingApp.init)
  document.addEventListener('DOMContentLoaded', RowSelection.init)
  document.addEventListener('DOMContentLoaded', BulkActions.init);
}