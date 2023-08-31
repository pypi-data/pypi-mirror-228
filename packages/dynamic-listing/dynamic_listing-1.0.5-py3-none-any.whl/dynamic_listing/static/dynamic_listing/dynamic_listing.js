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


if (document.readyState !== 'loading' && document.body) {
  addFiltersToDynamicListingApp.init()
  RowSelection.init()
} else {
  document.addEventListener('DOMContentLoaded', addFiltersToDynamicListingApp.init)
  document.addEventListener('DOMContentLoaded', RowSelection.init)
}