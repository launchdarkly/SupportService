// Code to trigger A/B Testing on click
nps_call = ldclient.variation('show-nps-survery', false)

// Code to trigger A/B Testing
get_nps = document.getElementById("style_a") == null?document.getElementById("style_b") : document.getElementById("style_a")

get_nps.addEventListener('click', function() {
    ldclient.track('nps-completed');
    console.log("Track Event Sent to LD");
});

ldclient.flush();

function generateNpsButton(number) {
    return `
<label class="btn btn-primary nps-value">
    <input type="radio" name="options" id="${number}" autocomplete="off"> ${number}
</label>
`
};

// JQuery to populate NPS buttons
$(document).ready(function() {

    for(i=1;i<=10;i++){
        $("#nps_container").append(generateNpsButton(i));
    }

    var cycle_div = ["nps_b_start", "nps_b_score", "nps_b_improve", "nps_b_features"],
        current_div = 0;

    function cycle_back(){
        if(current_div == 1){
            document.getElementById("backButton").style.display = "none";
        }
        document.getElementById(cycle_div[current_div]).style.display = "none";
        document.getElementById(cycle_div[current_div - 1]).style.display = "block";
        current_div -= 1;
    };

    function cycle_forward(){
        if(current_div == (cycle_div.length - 2))  {
            document.getElementById("nextButton").style.display = "none";
            document.getElementById("style_b").style.display = "block";
        }
        document.getElementById(cycle_div[current_div]).style.display = "none";
        document.getElementById(cycle_div[current_div + 1]).style.display = "block";
        current_div += 1;
    };

    $("#nextButton").click(function(){
        if(current_div <= 2){
            cycle_forward();
        }
        document.getElementById("backButton").style.display = "block";
    });

    $("#backButton").click(function(){
        if(current_div == 3){
            document.getElementById("nextButton").style.display = "block";
        }

        if (current_div > 0) {
        cycle_back();
        }

        if(current_div == 2){
            document.getElementById("style_b").style.display = "none";
        }

    });
});
