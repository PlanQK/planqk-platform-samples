package de.stoneone.planqk.samples;

import de.stoneone.planqk.api.CommunityAlgorithmsApi;
import de.stoneone.planqk.api.TaxonomiesApi;
import de.stoneone.planqk.api.invoker.ApiClient;
import de.stoneone.planqk.api.model.AlgorithmDto;
import de.stoneone.planqk.api.model.TaxonomyElement;
import de.stoneone.planqk.api.model.UpdateAlgorithmRequest;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class AlgorithmAddQuantumComputationModelSample {

    public static void main(String[] args) {
        String token = "Your personal access token";
        ApiClient apiClient = new ApiClient("apiKey", token);

        CommunityAlgorithmsApi algorithmApi = apiClient.buildClient(CommunityAlgorithmsApi.class);
        TaxonomiesApi taxonomiesApi = apiClient.buildClient(TaxonomiesApi.class);

        // Required attributes to create an algorithm
        String name = "My Algorithm";
        AlgorithmDto.ComputationModelEnum computationModel = AlgorithmDto.ComputationModelEnum.QUANTUM;

        AlgorithmDto payload = new AlgorithmDto()
            .name(name)
            .computationModel(computationModel);
        AlgorithmDto algorithm = algorithmApi.createAlgorithm(payload);

        algorithm = algorithmApi.getAlgorithm(algorithm.getId());

        // Retrieve a list of available quantum computation models
        List<TaxonomyElement> quantumComputationModels = taxonomiesApi.getQuantumComputationModels();

        // Retrieve Quantum Annealing from the list
        TaxonomyElement quantumAnnealing = quantumComputationModels.stream()
            .filter(taxonomyElement -> "Quantum Annealing".equalsIgnoreCase(taxonomyElement.getLabel()))
            .findFirst()
            .orElseThrow();

        /*
         * Adds quantum computation models to the algorithm
         */

        // Create the update request payload
        UpdateAlgorithmRequest updateAlgorithmRequest = new UpdateAlgorithmRequest()
            .name(name)
            .computationModel(UpdateAlgorithmRequest.ComputationModelEnum.QUANTUM)
            .quantumComputationModelUuids(Collections.singletonList(quantumAnnealing.getUuid()));
        algorithm = algorithmApi.updateAlgorithm(algorithm.getId(), updateAlgorithmRequest);

        //Remove all assigned quantum computation models
        updateAlgorithmRequest.quantumComputationModelUuids(new ArrayList<>());
        algorithm = algorithmApi.updateAlgorithm(algorithm.getId(), updateAlgorithmRequest);

    }
}
