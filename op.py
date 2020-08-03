# -*- encoding : utf-8 -*

# author  : Dr Mokira
# created : 2020-08-02
# updated : 2020-08-02

import time

from multiprocessing import Process
from multiprocessing import Queue
from multiprocessing import Value



"""
"""


class Operating( object ) :

	def __init__( self ) :
		super( Operating, self ).__init__();

		# Liste des arguments :
		self._argv = ();

		# Dictionnaire de paramètres :
		self._kwargv = {};

		# Queue de log :
		self._log = Queue();

		# Variable du poids de tâches :
		self._weight_var = Value( 'd', 0.0 );

		# Variable de progression :
		self._progress_var = Value( 'd', 0.0 );

		# Processus de calcul :
		self._process = None

		# Variable qui indique si l'opération est déjà en cour d'exécution :
		self._is_running = False;




	@property
	def argv( self ) :
		return self._argv;



	@property
	def kwargv( self ) :
		return self._kwargv;



	@property
	def weight( self ) :
		return self._weight_var.value;



	@property
	def progressv( self ) :
		return self._progress_var.value;



	@property
	def isrunning( self ) :
		return self._is_running
	



	def __call__( self, *_argv_, **_kwargv_ ) :
		self._argv   = _argv_   ;
		self._kwargv = _kwargv_ ;

		return self ;



	def getLog( self ) :
		return self._log.get() if not self._log.empty() else "";



	def increaseWeight( self, _w_=1 ) :
		self._weight_var.value += _w_;



	def decreaseWeight( self, _w_=1 ) :
		self._weight_var.value -= _w_;



	def progress( self, _w_=None ) :
		if _w_ is not None :
			if  _w_ >= 0 and ( ( self.progressv + _w_ )  <= self.weight ) :
				self._progress_var.value += _w_;

		else :
			self._progress_var.value += self.weight * 0.01 ;



	def regress( self, _w_=None ) :
		if _w_ is not None :
			if  _w_ >= 0 and ( ( self.progressv - _w_ )  >= 0 ) :
				self._progress_var.value -= _w_;

		else :
			self._progress_var.value -=  self.weight / 0.01 ;



	def print( self, _msg_ ) :
		_log.put( _msg_ );



	def onStart( self ) :
		pass;



	def run( self ) :
		raise NotImplementedError;



	def start( self ) :
		if not self.isrunning :
			self.onStart();
			self._process = Process( target=self.run );
			self._process.start();
			self._is_running = True;
			return self.isrunning;




	def restart( self ) :
		if self.isrunning :
			# On arrête :
			self._process.terminate();
			
			# On attend pendant 100 ms :
			time.sleep( 0.1 );

			# On démarrer à nouveau :
			self._process = Process( target=self.run );
			self._process.start();

			return True;




	def waitEnd( self ) :
		self._process.join();




	def stop( self ) :
		if self.isrunning :
			self._process.terminate();
			self._is_running = False;
			return True;

#end









if __name__ == '__main__' :
	import time

	class printing( Operating ) :

		def __init__( self ) :
			super( printing, self ).__init__();


		def run( self ) :
			n = self.argv[0];

			for i in range( n ) :
				print( f"Printing i : {i}" );
				time.sleep( 1 );

	#end

	p = printing();

	p( 15 ).start();
	print( "Lauch ..." );

#	time.sleep( 5 );
	p.waitEnd();
	print( "Terminated." );










































































































