# -*- encoding : utf-8 -*

# author  : Dr Mokira
# created : 2020-08-02
# updated : 2020-08-02

import os
import time

from datetime 	import datetime
from op 		import Operating



class Monitoring( Operating ) :

	def __init__( self, _mon_ ) :
		super( Monitoring, self ).__init__();
		
		# On ajoute un objet, ici le moniteur :
		self._mon = _mon_;

		# Configurations :
		self._config = {};

		# Création des configurations :
		self._config['DELAY']          = 0.5;
		self._config['SHOW_STATE_BAR'] = True;


	def config( self, name, value=None ) :
		if value is not None :
			self._config[name] = value;

			# On redémarre le monitoring :
			self.restart();

		else :
			return self._config[name];


	# Overide :
	def onStart( self ) :
		# On ajoute un attribut pour stocker le temps de départ :
		self._start_time = time.time();


	# Overide
	def run( self ) :

		# On utilise une boucle infinie s'il y a de données :
		while True :
			# On affiche l'état des variables :
			self._mon.show();

			# On affiche la barre de temps si possible :
			if self.config( 'SHOW_STATE_BAR' ) :
				print( "\n\t- during : ", int( time.time() - self._start_time ), "s", "- datetime : ", datetime.now() );

			# On se repose pendant {delay} secondes avant le prochain tour de boucle :
			time.sleep( self.config( 'DELAY' ) );


#end




class Monitor( object ) :

	def __init__( self ) :
		super( Monitor, self ).__init__();

		# Objet :
		self._object = None;

		# Dictionnire des champs :
		self._fields = {};

		# Taille max du nom des attributs :
		self._strmaxlen = 0;

		# Operation de monitoring :
		self.monitoring = Monitoring( self );

		# Configurations :
		self._config = {};




	def connect( self, _obj_ ) :
		self._object = _obj_;




	def addField( self, label, fieldname ) :
		if self._object :
			if fieldname in dir( self._object ) :
				self._strmaxlen     = self._strmaxlen if len( label ) <= self._strmaxlen else len( label );
				self._fields[label] = fieldname;

				# On redémarre le monitoring :
				self.monitoring.restart();

			else :
				print( "[ERROR]\t Attribute {fieldname} not found !" );
				return ;

			return True;
		else :
			print( "[ERROR]\t Monitor is not connected to object !" );



	def removeField( self, label ) :
		if label in self._fields :
			del self._fields[label];

			# On redémarre le monitoring :
			self.monitoring.restart();

		#end



	def valueOf( self, attrname ) :
		return getattr( self._object, attrname );




	def format( self, attrname, value ) :
		return "{}".format( value );



	def print( self, fields ) :
		for key, val in fields.items() :
			print( f"{key:{self._strmaxlen}}\t", self.format( val, self.valueOf( val ) ) );



	def printf( self ) :
		if self._object :

			if self._fields :
				self.print( self._fields );

			else :
				print( "\t\t[ NO DATA ]" );

			return True;

		else :
			print( "[ERROR]\t Monitor is not connected to object !" );
	#


	def show( self ) :
		# On efface la console :
		os.system( 'clear' if os.name != 'nt' else 'cls' );
		
		# On imprime les données si il y en a :
		self.printf();


	def config( self, name, value=None ) :
		if value is not None :
			self._config[name] = value;

			# On redémarre le monitoring :
#			self.monitoring.restart();

		else :
			return self._config[name];



#end



if __name__ == '__main__' :

	class Person( object ) :
		def __init__( self ) :
			self.name = "Titor";
			self.age  = 90;


	per = Person();
	mon = Monitor();


	mon.connect( per );
#	mon.addField( 'Person name', 'name' );
#	mon.addField( 'Person age',  'age' );

	mon.show();

	mon.monitoring.start();

	time.sleep( 5 );

	mon.addField( 'Person name', 'name' );
	mon.addField( 'Person age',  'age' );


	time.sleep( 5 );

	mon.monitoring.config( 'DELAY', 0.25 )  ;
	mon.monitoring.config( 'SHOW_STATE_BAR', False );

	time.sleep( 10 );

	mon.monitoring.stop();

	print( "Monitoring is stoped for 2 sec. " );
	time.sleep( 2 );

	mon.monitoring.start();

	print( "Monitoring is started ." );

	time.sleep( 10 );

	mon.monitoring.stop();
















































































































