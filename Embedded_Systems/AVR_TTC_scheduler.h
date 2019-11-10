/*
 * AVR_TTC_scheduler.h
 *
 *	Created: 8-11-2019 22:33:54
 *  Bron: Blackboard 2.1  Computer Systems - A&C
 */

// Scheduler data structure for storing task data
typedef struct
{
	// Pointer to task
	void (* pTask)(void);
	// Initial delay in ticks
	unsigned int Delay;
	// Periodic interval in ticks
	unsigned int Period;
	// Runme flag (indicating when the task is due to run)
	unsigned char RunMe;
} sTask;

// Function prototypes
//-------------------------------------------------------------------

void SCH_Init_T1(void);
void SCH_Start(void);
// Core scheduler functions
void SCH_Dispatch_Tasks(void);
unsigned char SCH_Add_Task(void (*)(void), const unsigned int, const unsigned int);
unsigned char SCH_Delete_Task(const unsigned char);

// hier het aantal taken aanpassen ....!!
// Maximum number of tasks

#define SCH_MAX_TASKS (5)
