// Copyright (c) 2017, C0D1G0 B1NAR10 and contributors
// For license information, please see license.txt

frappe.ui.form.on('Caja', {
	refresh: function(frm) {
		$('.ayudachico').hide();
	  $('.ayudagrande').hide();

	  $('.page-actions').prepend('<button data-video-id="0oBj2yMdXxg"  class="btn-xs js-modal-btn ayudagrande "><i class="far fa-question-circle"></i>  Ayuda</button>');
	  $(".js-modal-btn").modalVideo();
	}
});
