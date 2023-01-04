package de.stoneone.planqk.samples;

import de.stoneone.planqk.api.CommunityAlgorithmsApi;
import de.stoneone.planqk.api.invoker.ApiClient;
import de.stoneone.planqk.api.model.AlgorithmDto;
import de.stoneone.planqk.api.model.UpdateAlgorithmRequest;

public class AlgorithmUpdateSample {

    public static void main(String[] args) {
        String token = "Your personal access token";
        ApiClient apiClient = new ApiClient("apiKey", token);

        CommunityAlgorithmsApi algorithmApi = apiClient.buildClient(CommunityAlgorithmsApi.class);

        // Required attributes to create an algorithm
        String name = "My Algorithm";
        AlgorithmDto.ComputationModelEnum computationModel = AlgorithmDto.ComputationModelEnum.CLASSIC;

        AlgorithmDto payload = new AlgorithmDto()
            .name(name)
            .computationModel(computationModel);
        AlgorithmDto algorithm = algorithmApi.createAlgorithm(payload);

        algorithm = algorithmApi.getAlgorithm(algorithm.getId());

        /*
         * Updates several attributes of the algorithm
         */
        name = "Updated algorithm name";
        UpdateAlgorithmRequest.ComputationModelEnum updatedComputationModel = UpdateAlgorithmRequest.ComputationModelEnum.HYBRID;
        String acronym = "ALG";
        String intent = "algorithm intent";
        String problem = "algorithm problem";
        String algoParameter = "algorithm parameters";
        String inputFormat = "algorithm input format";
        String outputFormat = "algorithm output format";
        String solution = "algorithm solution";
        String assumptions = "algorithm assumptions";
        Boolean nisqReady = true;
        String speedUp = "unknown";

        // Create the update request payload
        UpdateAlgorithmRequest updateAlgorithmRequest = new UpdateAlgorithmRequest()
            .name(name)
            .computationModel(updatedComputationModel)
            .acronym(acronym)
            .intent(intent)
            .problem(problem)
            .algoParameter(algoParameter)
            .inputFormat(inputFormat)
            .outputFormat(outputFormat)
            .solution(solution)
            .assumptions(assumptions)
            .nisqReady(nisqReady)
            .speedUp(speedUp);

        algorithm = algorithmApi.updateAlgorithm(algorithm.getId(), updateAlgorithmRequest);

    }
}
