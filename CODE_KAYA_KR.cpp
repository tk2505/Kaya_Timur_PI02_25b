#include <iostream>
#include <vector>
#include <algorithm>
#include <random>
#include <chrono>
using namespace std;

// Функция вычисления длины маршрута
double routeLength(const vector<int>& route, const vector<vector<int>>& dist) {
    double length = 0;
    for (size_t i = 0; i < route.size() - 1; ++i)
        length += dist[route[i]][route[i + 1]];
    length += dist[route.back()][route[0]];
    return length;
}

// Вспомогательная функция для вычисления приспособленности
vector<double> calcFitness(const vector<vector<int>>& population, const vector<vector<int>>& dist) {
    vector<double> fitness(population.size());
    for (size_t i = 0; i < population.size(); ++i)
        fitness[i] = 1.0 / routeLength(population[i], dist);
    return fitness;
}

// Инициализация популяции
vector<vector<int>> initPopulation(int popSize, int n) {
    vector<vector<int>> population;
    vector<int> base(n);
    for (int i = 0; i < n; ++i) base[i] = i;
    for (int i = 0; i < popSize; ++i) {
        vector<int> ind = base;
        random_shuffle(ind.begin(), ind.end());
        population.push_back(ind);
    }
    return population;
}

// Турнирный отбор
int tournamentSelect(const vector<double>& fitness, int tournamentSize, mt19937& rng) {
    uniform_int_distribution<int> dist(0, fitness.size() - 1);
    int best = dist(rng);
    for (int i = 1; i < tournamentSize; ++i) {
        int candidate = dist(rng);
        if (fitness[candidate] > fitness[best])
            best = candidate;
    }
    return best;
}

// OX-кроссовер
vector<int> orderedCrossover(const vector<int>& parent1, const vector<int>& parent2, mt19937& rng) {
    int n = parent1.size();
    vector<int> child(n, -1);
    uniform_int_distribution<int> dist(0, n - 1);
    int a = dist(rng), b = dist(rng);
    if (a > b) swap(a, b);
    for (int i = a; i <= b; ++i)
        child[i] = parent1[i];
    int cur = (b + 1) % n, j = (b + 1) % n;
    while (cur != a) {
        while (find(child.begin(), child.end(), parent2[j]) != child.end())
            j = (j + 1) % n;
        child[cur] = parent2[j];
        cur = (cur + 1) % n;
    }
    return child;
}

// Мутация перестановкой (swap mutation)
void mutate(vector<int>& individual, mt19937& rng) {
    uniform_int_distribution<int> dist(0, individual.size() - 1);
    int a = dist(rng), b = dist(rng);
    swap(individual[a], individual[b]);
}

// Главная функция ГА
vector<int> gaTsp(const vector<vector<int>>& dist, int popSize, int generations, double mutationRate, int tournamentSize) {
    mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());
    int n = dist.size();
    vector<vector<int>> population = initPopulation(popSize, n);
    vector<double> fitness = calcFitness(population, dist);

    for (int gen = 0; gen < generations; ++gen) {
        vector<vector<int>> newPopulation;
        for (int i = 0; i < popSize; ++i) {
            // Турнирный отбор родителей
            int p1 = tournamentSelect(fitness, tournamentSize, rng);
            int p2 = tournamentSelect(fitness, tournamentSize, rng);
            // OX-кроссовер
            vector<int> child = orderedCrossover(population[p1], population[p2], rng);
            // Мутация
            uniform_real_distribution<double> mprob(0.0, 1.0);
            if (mprob(rng) < mutationRate)
                mutate(child, rng);
            newPopulation.push_back(child);
        }
        population = newPopulation;
        fitness = calcFitness(population, dist);
    }
    // Поиск лучшего индивида
    int bestInd = 0;
    double bestFit = fitness[0];
    for (int i = 1; i < popSize; ++i) {
        if (fitness[i] > bestFit) {
            bestFit = fitness[i];
            bestInd = i;
        }
    }
    return population[bestInd];
}

int main() {
    int n;
    cout << "Введите количество городов: ";
    cin >> n;
    vector<vector<int>> dist(n, vector<int>(n));
    cout << "Введите матрицу расстояний (" << n << "x" << n << "):\n";
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            cin >> dist[i][j];
int popSize, generations, tournamentSize;
    double mutationRate;
    cout << "Введите размер популяции: ";
    cin >> popSize;
    cout << "Введите количество поколений: ";
    cin >> generations;
    cout << "Введите вероятность мутации (например, 0.2): ";
    cin >> mutationRate;
    cout << "Введите размер турнира: ";
    cin >> tournamentSize;

    vector<int> best = gaTsp(dist, popSize, generations, mutationRate, tournamentSize);

    cout << "Лучший маршрут:\n";
    for (int x : best)
        cout << x + 1 << " ";
    cout << best[0] + 1 << "\n";
    cout << "Длина маршрута: " << routeLength(best, dist) << endl;

    return 0;
}

//Ввод: 4
//0 10 15 20
//10 0 35 25
//15 35 0 30
//20 25 30 0
//20 100 0.2 3 

//Вывод:
//Лучший маршрут: 1 3 4 2 1
//Длина маршрута: 80