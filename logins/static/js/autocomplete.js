$(function() {
  $('input.autocomplete').autocomplete({
    data: {
      "Agartala": null,
      "Ahemdabad": null,
      "Amritsar": null,
      "Bengaluru": null,
      "Chandigarh": null,
      "Chennai":null,
      "Coimbatore":null,
      "Cochin": null,
      "Hyderabad": null,
      "Lucknow": null,
      "Patana":null,
      "Varanasi":null
    },
    limit: 3, // The max amount of results that can be shown at once. Default: Infinity.
    onAutocomplete: function(val) {
      // Callback function when value is autcompleted.
    },
    minLength: 1, // The minimum length of the input for the autocomplete to start. Default: 1.
  });
});
