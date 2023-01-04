package de.stoneone.planqk.samples;

import de.stoneone.planqk.api.CommunityAlgorithmsApi;
import de.stoneone.planqk.api.invoker.ApiClient;
import de.stoneone.planqk.api.model.AlgorithmDto;
import de.stoneone.planqk.api.model.PageAlgorithmDto;
import java.util.ArrayList;
import java.util.List;

public class AlgorithmFindAndDeleteSample {

    public static void main(String[] args) {
        String token = "Your personal access token";
        ApiClient apiClient = new ApiClient("apiKey", token);

        CommunityAlgorithmsApi algorithmApi = apiClient.buildClient(CommunityAlgorithmsApi.class);

        //Query params that can be used to fetch the page of algorithms
        String search = ""; // parameter to filter the algorithms by name or acronym
        Integer page = 0; // Zero-based page index, allows to fetch a specific page
        Integer size = 30; // The size of the page to be returned
        List<String> sort = new ArrayList<>(); // Sorting criteria in the format: (asc|desc). Default sort order is ascending.

        // Either use "getAlgorithm(...)" to look-up by id, or search for it by name, which is what we show next
        //Get page of algorithms
        PageAlgorithmDto algorithms = algorithmApi.getAlgorithms(search, page, size, sort);

        String name = "My Algorithm";

        // Filter the list by name
        AlgorithmDto algorithm = algorithms.getContent().stream()
            .filter(a -> name.equalsIgnoreCase(a.getName()))
            .findFirst()
            .orElseThrow();

        // Deletes the algorithm
        algorithmApi.deleteAlgorithm(algorithm.getId());

    }
}
