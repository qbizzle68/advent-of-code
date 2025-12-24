#include <map>
#include <fstream>
#include <vector>
#include <string>
#include <iostream>


std::vector<std::string> import_data(const char* filepath) {
    std::ifstream f(filepath);
    if (!f.is_open()) {
        std::cerr << "Error opening file " << filepath << std::endl;
        exit(1);
    }

    std::vector<std::string> data;
    std::string line;
    while (std::getline(f, line)) {
        data.emplace_back(line);
    }

    return data;
}

// Result will be a massive number so need to use consistently large type
// to avoid any overflow.
typedef long long map_data_t;

map_data_t compute(const std::vector<std::string>& diagram) {
    int start_column;
    start_column = diagram[0].find('S');
    if (start_column == std::string::npos) {
        std::cerr << "Unable to find start position (no 'S' character found)\n";
        exit(2);
    }
    
    std::array<int, 2> coordinate = {1, start_column};
    std::map<std::array<int, 2>, map_data_t> beam_positions;
    beam_positions[coordinate] = 1;

    map_data_t count = 0;
    for (int i = 0; i < diagram.size() - 1; i++) {
        for (int j = 0; j < diagram[0].size(); j++) {
            if (beam_positions[{i, j}] > 0) {
                count = beam_positions[{i, j}];
                if (diagram[i + 1][j] == '^') {
                    beam_positions[{i, j}] = 0;
                    beam_positions[{i + 1, j - 1}] += count;
                    beam_positions[{i + 1, j + 1}] += count;
                } else {
                    beam_positions[{i, j}] = 0;
                    beam_positions[{i + 1, j}] += count;
                }
            }
        }
    }

    int last_row_index = diagram.size() - 1;
    size_t columns = diagram[0].size();
    map_data_t sum = 0;
    for (int i = 0; i < columns; i++) {
        sum += beam_positions[{last_row_index, i}];
    }

    return sum;
}


int main(int argc, char** argv) {
    if (argc != 2) {
        printf("Usage: %s FILEPATH\n", argv[0]);
        return 1;
    }
    const char* filepath = argv[1];
    std::vector<std::string> data = import_data(filepath);

    map_data_t result = compute(data);
    std::cout << "Result is " << result << "\n";

    return 0;
}
