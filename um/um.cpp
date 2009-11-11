#include <vector>
#include <iostream>
#include <fstream>
#include <ios>
#include <time.h>
#include <iterator>

class MemPool
{
private:
	MemPool();
	unsigned int* p;
public:
	MemPool(unsigned int* program, unsigned int size)
	{ 
		p = (unsigned int*)allocate(size);
		memcpy(&p[1], program, size * sizeof(unsigned int));
	}

	inline unsigned int* getEF(unsigned int i) 
	{ 
		return &p[i+1]; 
	}

	inline unsigned int* operator[](unsigned int i)
	{
		if (i == 0)
		{
			return p + 1;
		}
		return ((unsigned int*)i) + 1;
	}

	inline unsigned int allocate(unsigned int size)
	{
		unsigned int* r = new unsigned int[size+1];
		r[0] = size;
		memset(&r[1], 0, size * sizeof(unsigned int));
		return (unsigned int)r;
	}

	inline void deallocate(unsigned int i)
	{
		delete[] ((unsigned int*)i);
	}

	inline void load(unsigned int from)
	{
		if (from == 0)
		{
			return;
		}
		unsigned int* f = (unsigned int*)from;
		delete[] p;
		p = new unsigned int[f[0]+1];
		memcpy(p, f, (f[0]+1) * sizeof(unsigned int));
	}
};

#define OP (op >> 28)
#define A r[((op >> 6) & 0x7)]
#define B r[((op >> 3) & 0x7)]
#define C r[(op & 0x7)]
#define SA ((op >> 25) & 0x7)
#define SB (op & 0X1FFFFFF)

void interpret(unsigned int* boot, unsigned int size)
{
    unsigned int r[8] = {0,0,0,0,0,0,0,0};
    MemPool pa(boot, size);
	unsigned int* ef = pa.getEF(0);

#ifdef STORE_OUTPUT
	std::fstream f("out.bin", std::ios::out|std::ios::binary);
#endif
    while (1)
	{
		unsigned int op = *ef;
        switch(OP)
		{
        case 0:
            if (C)
                A = B;
            ++ef;
			break;
        case 1:
            A = pa[B][C];
            ++ef;
			break;
        case 2:
            pa[A][B] = C;
            ++ef;
			break;
        case 3:
            A = B + C;
            ++ef;
			break;
        case 4:
            A = B * C;
            ++ef;
			break;
        case 5:
            A = B / C;
            ++ef;
			break;
        case 6:
            A = ~(B & C);
            ++ef;        
			break;
        case 7:
			return;
        case 8:
            B = pa.allocate(C);
            ++ef;
			break;
        case 9:
			pa.deallocate(C);
            ++ef;
			break;
        case 10:
			std::cout << (char)C;
			std::cout.flush();
#ifdef STORE_OUTPUT
			f << (char)C;
			f.flush();
#endif
            ++ef;
			break;
        case 11:
			{
				char c;
				std::cin.read(&c, 1);
				C = c;
				++ef;
			}
			break;
        case 12:
			if (B)
			{
				pa.load(B);
			}
            ef = pa.getEF(C);
			break;
        case 13:
            r[SA] = SB;
            ++ef;
			break;
        default:
			return;
		}
	}
}

int main(int argc, char** argv)
{
	std::vector<unsigned int> c;

	std::ifstream f(argv[1], std::ios::in|std::ios::binary);

//	std::copy(std::istream_iterator<unsigned int>(f), std::istream_iterator<unsigned int>(), std::back_inserter(c));
	
	while (!f.eof())
	{
		unsigned char v[4];
		f.read((char*)v, 4);
		unsigned int s = ((v[0] << 24) + (v[1] << 16) + (v[2] << 8) + v[3]);
		c.push_back(s);
	};

	time_t before = time(0);
	interpret(&c[0], (unsigned int)c.size());
	time_t after = time(0);
	std::cout << "Finished in: " << after-before << " seconds" << std::endl;
	return 0;
}
    
