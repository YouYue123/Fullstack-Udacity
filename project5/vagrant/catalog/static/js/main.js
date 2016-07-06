



$(document).on("click", ".add_country_btn", function () {
			$('#modal_main_title').text('Add a new country')
			$('#modal_body_title').text('Country');
			$("#present_form").attr("action", "/country/new");
			$("#delete_btn").hide()
		    $('#present_modal').modal('show');
});

$(document).on("click", ".edit_country_btn", function () {
			var country_id = $(this).data('id');
			var country_name = $(this).data('name');
			$('#modal_main_title').text('Edit Country Information')
			$('#modal_body_title').text('Country');
			$("#name").val( country_name );
			$("#present_form").attr("action", "/country/"+ country_id +"/edit");
			$("#delete_btn").attr("onclick","deleteCountry(" + country_id  +")")
		    $('#present_modal').modal('show');
});


function deleteCountry(country_id){
	
	$.ajax({
		type: 'POST',
		url: '/country/' + country_id + '/delete',
		content:'application/octet-stream;charset=utf-8',
		success: function(result){
			window.location.href="/";
		}
	});

}

$(document).on('click',".addClubBtn",function(){
	var country_id = $(this).data('id')
	$('#modal_main_title').text('Add a new club')
		$('#modal_body_title').text('Club');
		$("#present_form").attr("action", "/country/"+country_id+"/football_club/new");
		$("#delete_btn").hide()
		$('#present_modal').modal('show');

});

$(document).on('click',".edit_club_btn",function(){
	
	var club_id = $(this).data('id');
		var club_name = $(this).data('name');
		var country_id = $(this).data('country')
		$('#modal_main_title').text('Edit Club Information')
		$('#modal_body_title').text('Club');
		$("#name").val( club_name );
		$("#present_form").attr("action", "/country/"+ country_id +"/football_club/"+ club_id  +"/edit");
		$("#delete_btn").attr("onclick","deleteClub(" + country_id + "," + club_id + ")")
		$('#present_modal').modal('show');

});

function deleteClub(country_id,club_id){
	$.ajax({
		type: 'POST',
		url: '/country/' + country_id + "/football_club/" + club_id + "/delete",
		content: 'application/octet-stream; charset=utf-8',
		success:function(result){
			window.location.href = "/country/" + country_id + "/football_club";
		}
	});
}