import { interval } from './constants.js'

window.onload =  function() {
    let startButtons = $('.start-btn')
    for (let i = 0; i < startButtons.length; i++) {
        startButtons[i].addEventListener('click', startTest);
    }
}

// cycled AJAX request for updating process (test run) status
  $(document).ready(function() {
    let refresh_id = setInterval(function() {
        $.get(
        "/status",
        function(data) {
            console.log(data);
            for (let key in data) {
                if (data[key] == 'completed') {
                    let dev_id = key
                    let button = $(`.start-btn.${dev_id}`)[0]
                    let statusIcon = $(`.status.${dev_id}`)[0]
                    if (statusIcon.getElementsByTagName('i').length > 0 ) {
                        statusIcon.getElementsByTagName('i')
                        testrunCompleted(statusIcon, button)
                    }
                    };
                };
            }
        )}
      , interval);
  });


function testRunStart(statusIcon, button) {
    button.disabled = true
    statusIcon.classList.remove('circle-green');
    if (statusIcon.getElementsByTagName('span').length> 0) {
        let resultCheckmark = statusIcon.getElementsByTagName('span')[0];
        statusIcon.removeChild(resultCheckmark)
    }
    let i = document.createElement('i');
    i.classList.add('fa', 'fa-spinner', 'fa-spin');
    statusIcon.appendChild(i);
}

// add testrun 'Passed' icon when tesrun is finished
//TODO: add 'Failed' icon, to show either Passed or Failed icon for each testrun according to its result
function testrunCompleted(statusIcon, button) {
    button.disabled = false
    let i = statusIcon.getElementsByTagName('i')[0]
    statusIcon.removeChild(i)
    statusIcon.classList.add('circle-green')
    let newSpan= document.createElement('span');
    let resultCheckmark = statusIcon.appendChild(newSpan)
    resultCheckmark.innerHTML = 'check';
    resultCheckmark.classList.add('material-symbols-outlined')
}

// collect the data from user inputs and send them to back end using post request
function startTest(event) {
    let deviceId = event.target.parentElement.className
    let button = event.target
    // add 'loading animation' to Testrun status column when testrun is in progress
    let statusIcon = $(`.status.${deviceId}`)[0]
    testRunStart(statusIcon, button)
    //
    let ip = $(`.ip.${deviceId}`)[0].value
    let password = $(`.password.${deviceId}`)[0].value
    let model = $(`.model.${deviceId}`)[0].innerHTML
    let firmware = $(`.firmware.${deviceId}`)[0].value
    let addDevice = $(`.add-dev.${deviceId}`)[0].value
    let testPath = $(`.test-path.${deviceId}`)[0].value

    if (testPath == "all") {
        testPath = 'tests'
    } else {
        testPath = `tests/${testPath}`
    };

    // send post request to backend with data collected from user inputs
    $.post("/postmethod", {
        dut: `--dut=${ip}`,
        password: `--password=${password}`,
        add_dev: `--additional-device=${addDevice}`,
        test_path: `${testPath}`,
        report_html: `${ip}report.html`,
        html_type: `--self-contained-html`,
        dev_id: `${deviceId}`
    });
}
