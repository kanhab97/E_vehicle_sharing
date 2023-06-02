
(function ($) {
    "use strict";

    // Sidebar Toggler
    $('.sidebar-toggler').click(function () {
        $('.sidebar, .content').toggleClass("open");
        return false;
    });
    
})(jQuery);

function openNav(){
    $('.sidebar, .content').toggleClass("open");
        return false;
}

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
let carr=[]
function onClickFunction(name,id){
    let vecs = {cname:name,cid:id}
    carr.push(vecs)
    console.log(carr)
}

function rechargebtn(){
    var vecs = document.querySelectorAll('.recvec');
        if(vecs.length == 0){
            message = "Select a vehicle to recharge"
            return response(400, message)
        } 
        else{
            for (var i = 0; i < vecs.length; i++) {   
                if(vecs[i].checked == true){
                    vehicle_id = vecs[i].id
                    vehicle = models.Vehicle.objects.filter(vehicle_id=vehicle_id).first()
                    vehicle.charge=100
                }  
            }
            vehicle.save()  
        }        
    // refresh
}
