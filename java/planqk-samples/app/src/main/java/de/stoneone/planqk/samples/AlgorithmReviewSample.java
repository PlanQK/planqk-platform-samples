package de.stoneone.planqk.samples;

import de.stoneone.planqk.api.CommunityAlgorithmsApi;
import de.stoneone.planqk.api.invoker.ApiClient;
import de.stoneone.planqk.api.model.AlgorithmDto;

public class AlgorithmReviewSample {

    public static void main(String[] args) {
        String token = "Your personal access token";
        ApiClient apiClient = new ApiClient("apiKey", token);

        CommunityAlgorithmsApi algorithmApi = apiClient.buildClient(CommunityAlgorithmsApi.class);

        AlgorithmDto payload = new AlgorithmDto()
            .name("My Algorithm")  // required
            .computationModel(AlgorithmDto.ComputationModelEnum.CLASSIC);  // required
        AlgorithmDto algorithm = algorithmApi.createAlgorithm(payload);

        algorithm = algorithmApi.getAlgorithm(algorithm.getId());

        // Starts the review of an algorithm by The PlanQK Expert Community
        algorithmApi.startReview(algorithm.getId());

        // Reviewed by PlanQK Expert Community
        algorithmApi.approveReview(algorithm.getId());

        // The review was withdrawn
        algorithmApi.withdrawReview(algorithm.getId());
    }
}
