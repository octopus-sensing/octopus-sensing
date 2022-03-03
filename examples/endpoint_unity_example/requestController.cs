using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;

public class requestController : MonoBehaviour

{
    public Button startStimuli;
    public Button stopStimuli;
    public Button terminateExperiment;

    // paramets to be sended to octopus sensing for the recording
    string _stimuli_id = "10"; // stimuli id, this should be changed according the stimuli presented to the user
    string _experiment_id = "00"; // experiment id 

    void Start()
    {
        // add listeners for each button, to know when their are pressed
        startStimuli.onClick.AddListener(startRequest);
        stopStimuli.onClick.AddListener(stopRequest);
        terminateExperiment.onClick.AddListener(terminateRequest);

    }

    // function to be executed when start button is pressed
    void startRequest()
    {
        Debug.Log("START PRESSED");

        // function to send the HTTP POST messages
        // when the to pass the "type of message" as a parameter
        StartCoroutine(Upload("START"));
    } 

    // function to be executed when stop button is pressed
    void stopRequest()
    {
        Debug.Log("STOP PRESSED");

        // function to send the HTTP POST messages
        // when the to pass the "type of message" as a parameter
        StartCoroutine(Upload("STOP"));
    }

    // function to be executed when terminate button is pressed
    void terminateRequest()
    {
        Debug.Log("TERMINATE PRESSED");

        // function to send the HTTP POST messages
        // when the to pass the "type of message" as a parameter
        StartCoroutine(Upload("TERMINATE"));
    }

    void Update()
    {
        
    }

    IEnumerator Upload(string type)
    {
        // format the JSON string to be sended
        // this have to include the "type of message", "experiment id" and, "stimuli id"
        string jsonData = "{\"type\":\"" + type + "\",\"experiment_id\":\"" + _experiment_id + "\",\"stimulus_id\":\"" + _stimuli_id + "\"}";

        // for TERMINATE messages, only the "type of message" is needed
        if (type == "TERMINATE")
        {
           jsonData = "{\"type\":\"TERMINATE\"}";
        }

        UnityWebRequest www = new UnityWebRequest("http://127.0.0.1:9331", "POST");

        // encode data in JSON format
        byte[] encodedPayload = new System.Text.UTF8Encoding().GetBytes(jsonData);
        www.uploadHandler = (UploadHandler)new UploadHandlerRaw(encodedPayload);
        www.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();

        // add headers to the request
        www.SetRequestHeader("Accept", "application/json");
        www.SetRequestHeader("Content-Type", "application/json");

        yield return www.SendWebRequest(); // send request

        // handling the response
        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            Debug.Log("Form upload complete!");
        }
    }
}
