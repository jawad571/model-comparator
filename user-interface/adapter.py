import requests
import json

yamtl_comparator_url = "http://localhost:8080"
nlp_comparator_url = "http://localhost:4040"
class Adapter:
    def compare_ecore_models_syntactically_and_semantically(groundTruthModelEcore, predictedModelEcore, config):
        model_level_json = {}
        class_level_json = {}

        ground_truth_model_emf = Adapter.get_emfatic_from_ecore(groundTruthModelEcore)
        predicted_truth_model_emf = Adapter.get_emfatic_from_ecore(predictedModelEcore)

        response_syntactic = Adapter.compare_ecore_models_syntactically(
            groundTruthModelEcore, predictedModelEcore, config)

        response_semantic = Adapter.compare_emfatic_models_semantically(ground_truth_model_emf, predicted_truth_model_emf)
        
        class_level_json = response_syntactic["classLevelJson"]
        model_level_json = {**response_syntactic["modelLevelJson"], **response_semantic, **response_syntactic["time"]}
        return model_level_json, class_level_json
            
    def compare_emfatic_models_syntactically_and_semantically(ground_truth_model_emf, predicted_truth_model_emf, config):
        model_level_json = {}
        class_level_json = {}

        groundTruthModelEcore = Adapter.get_ecore_model_from_emfatic(ground_truth_model_emf)
        predictedModelEcore = Adapter.get_ecore_model_from_emfatic(predicted_truth_model_emf)

        response_syntactic = Adapter.compare_ecore_models_syntactically(
            groundTruthModelEcore, predictedModelEcore, config)

        response_semantic = Adapter.compare_emfatic_models_semantically(ground_truth_model_emf, predicted_truth_model_emf)
        
        class_level_json = response_syntactic["classLevelJson"]
        model_level_json = {**response_syntactic["modelLevelJson"], **response_semantic, **response_syntactic["time"]}
        return model_level_json, class_level_json

    def compare_uml2_models_syntactically_and_semantically(ground_truth_model_uml2, predicted_truth_model_uml2, config):
        model_level_json = {}
        class_level_json = {}

        groundTruthModelEcore = Adapter.get_ecore_model_from_uml2(ground_truth_model_uml2)
        predictedModelEcore = Adapter.get_ecore_model_from_uml2(predicted_truth_model_uml2)
        
        ground_truth_model_emf = Adapter.get_emfatic_from_ecore(groundTruthModelEcore)
        predicted_truth_model_emf = Adapter.get_emfatic_from_ecore(predictedModelEcore)

        response_syntactic = Adapter.compare_ecore_models_syntactically(
            groundTruthModelEcore, predictedModelEcore, config)

        response_semantic = Adapter.compare_emfatic_models_semantically(ground_truth_model_emf, predicted_truth_model_emf)
        
        class_level_json = response_syntactic["classLevelJson"]
        model_level_json = {**response_syntactic["modelLevelJson"], **response_semantic, **response_syntactic["time"]}
        return model_level_json, class_level_json
    
    def compare_models_syntactically_and_semantically(
        ground_truth_model_ecore,
        predicted_model_ecore,
        ground_truth_model_emf, 
        predicted_truth_model_emf, 
        config
    ):
        model_level_json = {}
        class_level_json = {}

        response_syntactic = Adapter.compare_ecore_models_syntactically(ground_truth_model_ecore, predicted_model_ecore, config)
        response_semantic = Adapter.compare_emfatic_models_semantically(ground_truth_model_emf, predicted_truth_model_emf)
        
        class_level_json = response_syntactic["classLevelJson"]
        model_level_json = {**response_syntactic["modelLevelJson"], **response_semantic, **response_syntactic["time"]}
        return model_level_json, class_level_json
    
    def compare_emfatic_models_semantically(ground_truth_emfatic, predicted_emfatic):
        with open(ground_truth_emfatic, 'r') as groundTruthModel, open(predicted_emfatic, 'r') as predictedModel:
            groundTruthModelEmfatic = groundTruthModel.read()
            predictedModelEmfatic = predictedModel.read()
            nlp_comparator_endpoint = f'{nlp_comparator_url}/nlp-compare'
            response = requests.post(
                nlp_comparator_endpoint,
                headers={'Content-Type': 'application/json'},
                json={"groundTruthModelEmfatic": groundTruthModelEmfatic,
                    "predictedModelEmfatic": predictedModelEmfatic}
            )
            nlp_compare_result = response.text
            nlp_compare_result = json.loads(nlp_compare_result)
            return nlp_compare_result
    
    def compare_ecore_models_syntactically(ground_truth_model, predicted_model, config):
        with open(ground_truth_model, 'rb') as groundTruthModel, open(predicted_model, 'rb') as predictedModel, open(config, 'rb') as config_file:
            yamtl_comparator_endpoint = f'{yamtl_comparator_url}/compare'
            response = requests.post(
                yamtl_comparator_endpoint,
                files={
                    "groundTruthModel": groundTruthModel,
                    "predictedModel": predictedModel,
                    "config": config_file
                },
            )
            result = response.json()
        return result
    
    def get_ecore_model_from_emfatic(emfaticFilePath):
        comparator_url = f'{yamtl_comparator_url}/emfatic2ecore'
        with open(emfaticFilePath) as emfaticModel:
            ecoreFromEmfaticResponse = requests.post(
                comparator_url,
                files={"emfaticModel":emfaticModel}
            )

        ecore_path = emfaticFilePath.replace(".emf", ".ecore")
        with open(ecore_path, "w") as file:
            file.write(ecoreFromEmfaticResponse.text)  
        return ecore_path

    def get_ecore_model_from_uml2(umlFilePath):
        comparator_url = f'{yamtl_comparator_url}/uml2Toecore'
        with open(umlFilePath) as uml2Model:
            ecoreFromUml2Response = requests.post(
                comparator_url,
                files={"uml2Model":uml2Model}
            )

        ecore_path = umlFilePath.replace(".uml", ".ecore")
        with open(ecore_path, "w") as file:
            file.write(ecoreFromUml2Response.text)  
        return ecore_path
            
    def get_emfatic_from_ecore(ecoreModelFilePath):
        comparator_url = f'{yamtl_comparator_url}/ecore2emfatic'
        with open(ecoreModelFilePath) as emfaticModel:
            ecoreFromEmfaticResponse = requests.post(
                comparator_url,
                files={"ecoreModel":emfaticModel}
            )
        emf_path = ecoreModelFilePath.replace(".ecore", ".emf")
        with open(emf_path, "w") as file:
            file.write(ecoreFromEmfaticResponse.text)
        return emf_path
if __name__ == "__main__":
    print(Adapter.get_ecore_model_from_uml2("/mnt/mydrive/leicester/uol/thesis/repo/jm982/code/branches/model-comparator-main/syntactic-comparator/src/main/resources/sample_model.uml"))