
(function ($) {
    "use strict";

    // Sidebar Toggler
    $('.sidebar-toggler').click(function () {
        $('.sidebar, .content').toggleClass("open");
        return false;
    });
    
})(jQuery);


function repairbtn(){
    var vecs = document.querySelectorAll('.repvec');
        if(vecs.length == 0){
            message = "Select a vehicle to repair"
            return response(400, message)
        } 
        else{
            for (var i = 0; i < vecs.length; i++) {   
                if(vecs[i].checked == true){
                    vehicle_id = vecs[i].id
                    vehicle = models.Vehicle.objects.filter(vehicle_id=vehicle_id).first()
                    vehicle.repair_status=0
                    vehicle.repair_desc=""
                }  
            }
            vehicle.save()  
        }        
    // refresh
}


