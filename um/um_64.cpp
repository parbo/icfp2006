#include <vector>
#include <map>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <ios>
#include <time.h>
#include <string.h>

class Chunk
{
public:
	inline Chunk(unsigned int sz) : sz(sz) 
	{ 
		p = new unsigned int[sz]; 
		memset(p, 0, sz * sizeof(unsigned int)); 
	}
	Chunk(unsigned int* b, unsigned int sz) : sz(sz) 
	{ 
		p = new unsigned int[sz]; 
		memcpy(p, b, sz * sizeof(unsigned int)); 
	}
	~Chunk() 
	{ 
		delete[] p; 
	}
	inline unsigned int& operator[](unsigned int ix) 
	{ 
		return p[ix]; 
	}
	inline unsigned int operator[](unsigned int ix) const 
	{ 
		return p[ix]; 
	}
	inline unsigned int size() const 
	{ 
		return sz; 
	}
	inline void from(const Chunk* c) 
	{ 
		if (sz != c->sz) 
		{ 
			delete[] p; 
			sz = c->sz; 
			p = new unsigned int[sz]; 
		} 
		memcpy(p, c->p, sz * sizeof(unsigned int)); 
	}
private:
	Chunk();
	Chunk& operator=(const Chunk&);
	Chunk(const Chunk&);
	unsigned int* p;
	unsigned int sz;
};

class MemPool
{
private:
	MemPool();
	std::vector<Chunk*> m;
	std::vector<unsigned int> free;
public:
	MemPool(Chunk* program)
	{ 
		m.push_back(program);
	}

	inline unsigned int* getEF(unsigned int i) 
	{ 
		return &((*m[0])[i]); 
	}

	inline Chunk& operator[](unsigned int i)
	{
		return *m[i];
	}

	inline unsigned int allocate(unsigned int size)
	{
		if (free.size())
		{
			unsigned int ix = free.back();
			m[ix] = new Chunk(size);
			free.pop_back();
			return ix;
		}
		else
		{
			m.push_back(new Chunk(size));
			return m.size()-1;
		}
	}

	inline void deallocate(unsigned int i)
	{
		delete m[i];
		free.push_back(i);
	}

	inline void load(unsigned int from)
	{
		if (from)
		{
			m[0]->from(m[from]);
		}
	}
};

#define OP (op >> 28)
#define A r[((op >> 6) & 0x7)]
#define B r[((op >> 3) & 0x7)]
#define C r[(op & 0x7)]
#define SA ((op >> 25) & 0x7)
#define SB (op & 0X1FFFFFF)

void interpret(Chunk& boot)
{
    unsigned int r[8] = {0,0,0,0,0,0,0,0};
    MemPool pa(&boot);
	unsigned int* ef = pa.getEF(0);

    while (1)
	{
		unsigned int op = *ef;
        switch(OP)
		{
        case 0:
            if (C)
			{
                A = B;
			}
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
			pa.load(B);
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

	while (!f.eof())
	{
		unsigned char v[4];
		f.read((char*)v, 4);
		unsigned int s = ((v[0] << 24) + (v[1] << 16) + (v[2] << 8) + v[3]);
		c.push_back(s);
	};

	Chunk cc(&c[0], c.size());
	time_t before = time(0);
	interpret(cc);
	time_t after = time(0);
	std::cout << "Finished in: " << after-before << " seconds" << std::endl;
	return 0;
}

    
