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

    string stimuli_id = "10";
    string experiment_id = "00";

    void Start()
    {
        startStimuli.onClick.AddListener(startRequest);
        stopStimuli.onClick.AddListener(stopRequest);
        terminateExperiment.onClick.AddListener(terminateRequest);

    }

    void startRequest()
    {
        Debug.Log("START PRESSED");
        StartCoroutine(Upload("START"));
    } 

    void stopRequest()
    {
        Debug.Log("STOP PRESSED");
        StartCoroutine(Upload("STOP"));
    }

    void terminateRequest()
    {
        Debug.Log("TERMINATE PRESSED");
        StartCoroutine(Upload("TERMINATE"));
    }

    void Update()
    {
        
    }

    IEnumerator Upload(string type)
    {
        WWWForm form = new WWWForm();
        form.AddField("type", type);
        form.AddField("experiment_id", experiment_id);
        form.AddField("stimuli_id", stimuli_id);

        string jsonData = "{\"type\":\"" + type + "\",\"experiment_id\":\"" + experiment_id + "\",\"stimulus_id\":\"" + stimuli_id + "\"}";

        if (type == "TERMINATE")
        {
           jsonData = "{\"type\":\"TERMINATE\"}";
        }

        UnityWebRequest www = new UnityWebRequest("http://127.0.0.1:9331", "POST");
        byte[] encodedPayload = new System.Text.UTF8Encoding().GetBytes(jsonData);
        www.uploadHandler = (UploadHandler)new UploadHandlerRaw(encodedPayload);
        www.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
        www.SetRequestHeader("Accept", "application/json");
        www.SetRequestHeader("Content-Type", "application/json");

        yield return www.SendWebRequest();

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
