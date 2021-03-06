// Numerik0_Zettel1.cpp : Diese Datei enthält die Funktion "main". Hier beginnt und endet die Ausführung des Programms.
//

#include "pch.h"
#include <iostream>
#include <vector>
#include <math.h>

#define PI 3.1415926536

template <typename T>
//gebe den Vektor aus 
void vectorprint(T inp) {
	std::cout << "[";
	for (int i = 0; i < inp.size(); i++) {
		std::cout << inp[i] << ", ";
	}
	std::cout << "] " << std::endl;
}

template <typename T>
//gebe die Matrix aus 
void matrixprint(T inp) {
	std::cout << "[";
	for (int i = 0; i < inp.size(); i++) {
		vectorprint(inp[i]);
	}
	std::cout << "] " << std::endl;
}

template <typename T>
//gebe das Tupel aus 
void pairprint(T inp) {
	std::cout << "[";
	for (int i = 0; i < inp.size(); i++) {
		std::cout << "(" << inp[i].first << ", " << inp[i].second << ")" << ", ";
	}
	std::cout << "] " << std::endl;
}

double degree(double radians) {
	return radians * 180 / PI;
}

class neville {
private: 
	std::vector<double> x_n;
	double x;
	std::vector<std::pair<double,double>> grid_points; //Tupel der Gitternetzpunkte 
	std::vector<std::vector<double>> pik; //Vektor pik
	double n = 1;
public:
	//Konstruktor 1: berechnen mittels sin(x)
	neville(double new_x, std::vector<double> new_xn) // p(x) := (x; f; [x_0, ... , x_n])
		:
		x(new_x), //überge new_n an das private Mitglied x
		x_n(new_xn),
		grid_points(new_xn.size()), //grid_points bekommt seine Länge zugewiesen 
		// pik(x_n.size(), std::vector<double>(x_n.size()))
		pik(x_n.size()) //pik bekommt seine Länge zugewiesen 
	{
		//definiere das Tupel, uebergebe xn[i] an die erste Stelle und an die zweite die Auswertung an dem Punkt 
		for (int i = 0; i < new_xn.size(); i++) {
			grid_points[i].first = new_xn[i];
			grid_points[i].second = sin(new_xn[i]);
		}
		//definiere die erste Spalte der pik's 
		for (int i = 0; i < grid_points.size(); i++) {
			pik[0].push_back(grid_points[i].second);
			//pik[0][i] = grid_points[i].second;
		}
		//füge in der Matrix 0en ein, sodass in jeder Spalte immer eine Null dazukommt 
		for (int i = 0; i < x_n.size(); i++) {
			for (int j = 0; j < i; j++) {
				pik[i].push_back(0);
			}
		}
	}
	//Konstruktor 2: berechnen mittels sin(nx)
	neville(double new_x, std::vector<double> new_xn, double n) // p(x) := (x; f; [x_0, ... , x_n])
		:
		x(new_x),
		x_n(new_xn),
		grid_points(new_xn.size()),
		// pik(x_n.size(), std::vector<double>(x_n.size()))
		pik(x_n.size())
	{
		for (int i = 0; i < new_xn.size(); i++) {
			grid_points[i].first = new_xn[i];
			grid_points[i].second = sin(n * new_xn[i]);
		}
		for (int i = 0; i < grid_points.size(); i++) {
			pik[0].push_back(grid_points[i].second);
			//pik[0][i] = grid_points[i].second;
		}
		for (int i = 0; i < x_n.size(); i++) {
			for (int j = 0; j < i; j++) {
				pik[i].push_back(0);
			}
		}
	}
	void print() {
		vectorprint(x_n);
		pairprint(grid_points);
		matrixprint(pik); 
	}
	double berechne() {
		for (int k = 0; k < pik.size()-1; k++) {
			for (int i = k ; i < pik[k].size()-1; i++) {
				// std::cout << "i: " << i << " k: " << k << std::endl;
				double next_pik = pik[k][i + 1] + (x - grid_points[i + 1].first) / (grid_points[i + 1].first - grid_points[i - k].first) * (pik[k][i + 1] - pik[k][i]);
				// std::cout << next_pik << " = " << pik[k][i + 1] << " + " << "(" << degree(x) << " - " << degree(grid_points[i + 1].first) << ") / ( " << degree(grid_points[i + 1].first) << "-" << degree(grid_points[i - k].first) << ") * (" << pik[k][i + 1] << " - "<< pik[k][i] << ")" << std::endl;
				pik[k + 1].push_back(next_pik);
			}
		}
		return pik[pik.size() - 1][pik.size() - 1];
	}
};

double radians(double degree) {
	return degree * PI / 180;
}

int main() {
	float x = 45;
	x = radians(x);
	std::vector<double> x_n = {{ 0, 30, 60, 90 }};
	for (int i = 0; i < 4; i++) {
		x_n[i] = radians(x_n[i]);
	}
	//float px[4] =  {x * 180 / pi, sin[4], x_n}
	neville sin_interpol = neville(x, x_n);
	/* for (auto el : x_n) {
		std::cout << el << ", ";
	} */
	std::cout << std::endl;
	// sin_interpol.print();
	double result = sin_interpol.berechne();
	std::cout << "Das Ergebnis ist: " << result << std::endl;
	// sin_interpol.print();

	//create a scaled version of the sin() function 
	int n = 2;
	neville sin_interpol_2 = neville(x, x_n, n);
	int m = 4;
	neville sin_interpol_4 = neville (x, x_n, m); 
	int l = 8;
	neville sin_interpol_8 = neville(x, x_n, l);
	std::cout << "Das Ergebnis bei der Skalierung mit 2 ist: " << sin_interpol_2.berechne() << std::endl;
	std::cout << "Das Ergebnis bei der Skalierung mit 4 ist: " << sin_interpol_4.berechne() << std::endl; 
	std::cout << "Das Ergebnis bei der Skalierung mit 8 ist: " << sin_interpol_8.berechne() << std::endl;

	return 0;
}




	